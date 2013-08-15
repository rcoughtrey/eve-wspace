#    Eve W-Space
#    Copyright (C) 2013  Andrew Austin and other contributors
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version. An additional term under section
#    7 of the GPL is included in the LICENSE file.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule
from core.models import ConfigEntry

class Command(BaseCommand):
    """
    Load default settings from each application's default_settings.py file.
    """
    def handle(self, *args, **options):
        if not args:
            for app in settings.INSTALLED_APPS:
                mod = import_module(app)
                if module_has_submodule(mod, "default_settings"):
                    try:
                        def_mod = import_module("%s.default_settings" % app)
                        def_mod.load_defaults()
                    except:
                        raise
        else:
            for app in args:
                try:
                    mod = import_module(app)
                except ImportError:
                    raise CommandError('App %s could not be imported.' % app)
                if module_has_submodule(mod, "default_settings"):
                    try:
                        def_mod = import_module("%s.default_settings" % app)
                        def_mod.load_defaults()
                    except:
                        raise