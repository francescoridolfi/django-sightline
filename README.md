# django-sightline 🕵️‍♂️

**Smart, privacy-friendly site analytics for Django.** Track visits, popular pages, referrers, and more — directly from the admin dashboard.

## Features ✨

- 🔒 **Privacy-Focused**: Designed with user privacy in mind.
- 🛠️ **Admin Dashboard Integration** : View analytics directly within Django's admin interface.
- 📈 **Page Tracking**: Monitor page visits and identify popular content.
- 🔗 **Referrer Tracking**: Understand where your traffic is coming from.
- 🎨 **Customizable**: Easily extend and modify to fit your project's needs.

## 🚀 Next Steps

- 🔗 Add a referral system  
- ⚡ Reduce logging load in `VisitLog`  
- 🔍 Add filters in the admin panel  
- 📚 Implement documentation 


## Installation ⚙️

1. Install the package via pip:

   ```bash
   pip install django-sightline
   ```


2. Add `'sightline'` to your `INSTALLED_APPS` in `settings.py`:

   ```python
   INSTALLED_APPS = [
       ...
       'sightline',
       ...
   ]
   ```


3. Run migrations to set up the necessary database tables:

   ```bash
   python manage.py migrate sightline
   ```


4. Include the middlewares you need in your `MIDDLEWARE` settings:

   ```python
   MIDDLEWARE = [
       ...
       'sightline.middleware.VisitLogMiddleware',
       ...
   ]
   ```


5. Optionally, configure the `SIGHTLINE_SETTINGS` dicts to customize your tracking experience:

   ```python
   SIGHTLINE_SETTINGS = {
        "visit": {
            "enabled": True,
            "exclude_path": r"^/admin/",
            "interval_capturing": 5 # Seconds
        },
        "geoip": {
            "enabled": False,
            "marker_interval": 10 # days
        }
   }
   ```

![dashboard](dashboard.png)


## Usage 📝

Once installed, django-sightline automatically tracks page visits and referrers. You can view the analytics data in the Django admin interface under the "Sightline" section.

To customize the behavior, you can extend the provided models and middleware. For example, to track additional data or modify the tracking logic, customize your Admin Model with `BaseLogAdmin` and override the methods and criteria for metrics generation.

## Contributing 🤝

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License 🔑

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
