from django.db import models


class Menu(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    inventory = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title


class Booking(models.Model):
    name = models.CharField(max_length=100)
    no_of_guests = models.PositiveIntegerField()
    booking_date = models.DateTimeField()
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='bookings',
    )

    class Meta:
        ordering = ['booking_date']

    def __str__(self):
        return f'{self.name} - {self.booking_date:%Y-%m-%d %H:%M}'
