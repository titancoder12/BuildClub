from django import forms

from .models import Registration


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = [
            "student_first_name",
            "student_last_name",
            "student_grade",
            "guardian_name",
            "guardian_email",
            "notes",
            "consent",
        ]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs) -> None:
        self.course = kwargs.pop("course", None)
        super().__init__(*args, **kwargs)
        self.fields["consent"].required = True
        for name, field in self.fields.items():
            if name == "consent":
                field.widget.attrs.update(
                    {
                        "class": "mt-1 h-5 w-5 rounded border-slate-300 text-teal-500 focus:ring-teal-500"
                    }
                )
            elif name == "notes":
                field.widget.attrs.update(
                    {
                        "class": (
                            "mt-2 w-full rounded-2xl border border-slate-200 px-4 py-3 "
                            "text-sm text-slate-700 shadow-sm focus:border-teal-500 "
                            "focus:outline-none focus:ring-2 focus:ring-teal-200"
                        )
                    }
                )
            else:
                field.widget.attrs.update(
                    {
                        "class": (
                            "mt-2 w-full rounded-full border border-slate-200 px-4 py-3 "
                            "text-sm text-slate-700 shadow-sm focus:border-teal-500 "
                            "focus:outline-none focus:ring-2 focus:ring-teal-200"
                        )
                    }
                )

    def clean(self) -> dict:
        cleaned = super().clean()
        if self.course and self.course.is_full():
            raise forms.ValidationError(
                "This course is currently full. Please check back for future openings."
            )
        return cleaned
