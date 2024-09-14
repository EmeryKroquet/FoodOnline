from enum import unique

from django.core.exceptions import ValidationError
from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification
from datetime import time, datetime, date


class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=100, unique=True)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name

    def is_open(self):
        """
        This method checks whether the vendor is open by looking at the current time
        and comparing it with the stored opening hours.
        """
        today_date = date.today()
        today = today_date.isoweekday()  # Get the current day of the week (1=Monday, 7=Sunday)

        # Get today's opening hours for this vendor
        current_opening_hours = OpeningHour.objects.filter(vendor=self, day=today)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        is_open = False  # Default to False, assuming closed if no matching hours are found
        for opening_hour in current_opening_hours:
            if not opening_hour.is_closed:
                # Convert stored hours from 12-hour format (e.g., 02:30 PM) to 24-hour format
                start = str(datetime.strptime(opening_hour.from_hour, "%I:%M %p").time())
                end = str(datetime.strptime(opening_hour.to_hour, "%I:%M %p").time())
                if start <= current_time <= end:
                    is_open = True
                    break
        return is_open

    def save(self, *args, **kwargs):
        """
        Overriding the save method to send approval/rejection emails upon changing the vendor approval status.
        """
        if self.pk is not None:  # Only check for updates if the instance already exists (i.e., not on creation)
            original = Vendor.objects.get(pk=self.pk)
            if original.is_approved != self.is_approved:
                # Prepare the email content
                mail_template = 'accounts/emails/admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                    'to_email': self.user.email,
                }
                if self.is_approved:
                    mail_subject = "Congratulations! Your restaurant has been approved."
                else:
                    mail_subject = "We're sorry! You are not eligible for publishing your food menu on our marketplace."

                # Send notification email
                send_notification(mail_subject, mail_template, context)

        return super(Vendor, self).save(*args, **kwargs)


# Constants for days of the week and time slots
DAYS = [
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
    (7, "Sunday"),
]

# Generating a list of half-hour time slots in 12-hour format (AM/PM)
HOUR_OF_DAY_24 = [(time(h, m).strftime('%I:%M %p'), time(h, m).strftime('%I:%M %p')) for h in range(0, 24) for m in
                  (0, 30)]

class OpeningHour(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour = models.TimeField()
    to_hour = models.TimeField()
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('day', 'from_hour')
        unique_together = ('vendor', 'day', 'from_hour', 'to_hour')

    def __str__(self):
        return f'{self.get_day_display()} - {self.from_hour} to {self.to_hour}'

    def clean(self):
        """
        Validate that the opening time is before the closing time.
        """
        if self.from_hour >= self.to_hour and not self.is_closed:
            raise ValidationError('The opening time must be before the closing time.')

    def is_open_now(self):
        """
        Method to check if the vendor is open at the current time.
        """
        from datetime import datetime
        now = datetime.now().time()
        if not self.is_closed and self.from_hour <= now <= self.to_hour:
            return True
        return False