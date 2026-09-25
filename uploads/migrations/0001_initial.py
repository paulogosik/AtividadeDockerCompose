from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Arquivo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=255)),
                ("arquivo", models.FileField(max_length=300, upload_to="uploads/")),
                ("enviado_em", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-enviado_em"]},
        )
    ]
