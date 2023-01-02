from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
BRANCH_CHOICES = (
    ('COMP', 'Computer'),
    ('IT', 'Information Technology'),
    ('EXTC', 'Electronics & Telecommunication'),
    ('CIVIL', 'Civil'),
    ('MECH_A', 'Mechanical Section A'),
    ('MECH_B', 'Mechanical Section B'),
    ('INST', 'Instrumentation'),
    ('ASH', 'ASH Department'),
    ('AIDS', 'Artificial Inteligence & Data Science'),
    ('CSE/DS', 'Computer Science / Data Science')
)

YEAR_CHOICES = (
    ('FE', 'First Year'),
    ('SE', 'Second Year'),
    ('TE', 'Third Year'),
    ('BE', 'Fourth Year'),
    ('D', 'Departmental'),
)

PAYMENT_STATUS = (
    ('S', 'Successfully Done'),
    ('P', 'Pending'),
)

ENTRY_TYPE = (
    ('INTER', 'Inter College'),
    ('INTRA', 'Intra College'),
)


class Event(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[
        MinValueValidator(0)])
    no_limit = models.BooleanField(default=False)
    event_head = models.ForeignKey('account.Account', on_delete=models.CASCADE)
    contact_1 = models.CharField(max_length=10)
    contact_2 = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Entry(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE)
    type = models.CharField(max_length=5, choices=ENTRY_TYPE)
    college = models.CharField(max_length=1025)
    registered_by = models.ForeignKey(
        'account.Account', on_delete=models.CASCADE)
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=12)
    email = models.EmailField()
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES)
    class_name = models.CharField(
        max_length=3, choices=YEAR_CHOICES, null=True, blank=True)
    payment_status = models.CharField(max_length=2, choices=PAYMENT_STATUS)
    remark = models.TextField(null=True, blank=True)
    mark_as_used = models.BooleanField(default=False)
    register_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.code} : {self.get_branch_display()} - {self.name}'

    class Meta:
        verbose_name_plural = "Entries"


class Code(models.Model):
    assigned_to = models.ForeignKey(
        'account.Account', on_delete=models.CASCADE)
    code = models.CharField(max_length=255)
    sub_code = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self) -> str:
        return f'{self.code} - {self.assigned_to} - {self.is_active}'
