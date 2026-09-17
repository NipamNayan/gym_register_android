"""
Gym Registration System — Android (Kivy + KivyMD)
Offline, SQLite-backed, no internet required.
"""

import os
import sys
import datetime
import traceback

# --- Crash logger for Android debugging ---
def _setup_crash_log():
    """Redirect stderr to a crash log file on Android so we can diagnose failures."""
    try:
        from android.storage import app_storage_path
        log_dir = app_storage_path()
        if log_dir:
            crash_log = os.path.join(log_dir, "crash.log")
            sys.stderr = open(crash_log, "w")
    except Exception:
        pass

_setup_crash_log()

from database import Database

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, NumericProperty, ObjectProperty

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.list import TwoLineAvatarIconListItem, IconRightWidget, IconLeftWidget
from kivymd.uix.picker import MDDatePicker

KV = '''
#:import dp kivy.metrics.dp

<CustomerListItem>:
    on_release: app.on_customer_tap(self.customer_id)
    IconLeftWidget:
        icon: root.status_icon
        theme_text_color: "Custom"
        text_color: root.status_color

    IconRightWidget:
        icon: "delete"
        theme_text_color: "Custom"
        text_color: 1, 0.27, 0.27, 1
        on_release: app.confirm_delete(root.customer_id, root.text)


ScreenManager:
    HomeScreen:
    AddEditScreen:
    DetailScreen:


<HomeScreen>:
    name: "home"
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Gym Registration"
            elevation: 4
            right_action_items: [["plus-circle", lambda x: app.go_add()]]

        MDBoxLayout:
            orientation: "vertical"
            padding: dp(8)
            spacing: dp(4)

            MDTextField:
                id: search_field
                hint_text: "Search by name or phone"
                icon_right: "magnify"
                on_text: app.on_search(self.text)

            MDTabs:
                id: tabs
                on_tab_switch: app.on_tab_switch(*args)

                Tab:
                    id: tab_all
                    title: "All"
                    MDBoxLayout:
                        orientation: "vertical"
                        ScrollView:
                            MDList:
                                id: list_all
                        MDRaisedButton:
                            text: "EXPORT ALL (CSV)"
                            size_hint_y: None
                            height: dp(48)
                            on_release: app.export_csv("all")

                Tab:
                    id: tab_active
                    title: "Active"
                    MDBoxLayout:
                        orientation: "vertical"
                        ScrollView:
                            MDList:
                                id: list_active
                        MDRaisedButton:
                            text: "EXPORT ACTIVE (CSV)"
                            size_hint_y: None
                            height: dp(48)
                            on_release: app.export_csv("active")

                Tab:
                    id: tab_expired
                    title: "Expired"
                    MDBoxLayout:
                        orientation: "vertical"
                        ScrollView:
                            MDList:
                                id: list_expired
                        MDRaisedButton:
                            text: "EXPORT EXPIRED (CSV)"
                            size_hint_y: None
                            height: dp(48)
                            on_release: app.export_csv("expired")


<AddEditScreen>:
    name: "addedit"
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            id: form_toolbar
            title: "Add Customer"
            elevation: 4
            left_action_items: [["arrow-left", lambda x: app.go_home()]]

        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(16)
                spacing: dp(8)
                adaptive_height: True

                MDTextField:
                    id: name_field
                    hint_text: "Full Name *"
                    icon_right: "account"
                    mode: "rectangle"

                MDTextField:
                    id: age_field
                    hint_text: "Age *"
                    icon_right: "numeric"
                    input_filter: "int"
                    mode: "rectangle"

                MDTextField:
                    id: phone_field
                    hint_text: "Phone Number *"
                    icon_right: "phone"
                    input_filter: "int"
                    mode: "rectangle"

                MDBoxLayout:
                    adaptive_height: True
                    spacing: dp(8)

                    MDTextField:
                        id: date_field
                        hint_text: "Subscription Date *"
                        icon_right: "calendar"
                        mode: "rectangle"
                        readonly: True
                        on_focus: if self.focus: app.show_date_picker()

                    MDTextField:
                        id: period_field
                        hint_text: "Period (months)"
                        mode: "rectangle"
                        readonly: True

                MDBoxLayout:
                    adaptive_height: True
                    spacing: dp(8)
                    padding: [0, dp(4), 0, 0]
                    MDLabel:
                        text: "Subscription Period:"
                        adaptive_height: True

                MDGridLayout:
                    cols: 4
                    adaptive_height: True
                    spacing: dp(8)

                    MDRaisedButton:
                        text: "1 Mo"
                        on_release: app.set_period(1)
                    MDRaisedButton:
                        text: "3 Mo"
                        on_release: app.set_period(3)
                    MDRaisedButton:
                        text: "6 Mo"
                        on_release: app.set_period(6)
                    MDRaisedButton:
                        text: "12 Mo"
                        on_release: app.set_period(12)

                MDBoxLayout:
                    adaptive_height: True
                    spacing: dp(12)
                    padding: [0, dp(16), 0, 0]

                    MDRaisedButton:
                        id: save_btn
                        text: "SAVE"
                        md_bg_color: app.theme_cls.primary_color
                        on_release: app.save_customer()
                        size_hint_x: 1

                    MDFlatButton:
                        text: "CLEAR"
                        on_release: app.clear_form()
                        size_hint_x: 0.4


<DetailScreen>:
    name: "detail"
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Customer Details"
            elevation: 4
            left_action_items: [["arrow-left", lambda x: app.go_home()]]
            right_action_items: [["pencil", lambda x: app.go_edit()]]

        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(20)
                spacing: dp(12)
                adaptive_height: True

                MDCard:
                    padding: dp(16)
                    elevation: 4
                    adaptive_height: True
                    radius: [dp(12)]

                    MDBoxLayout:
                        orientation: "vertical"
                        adaptive_height: True
                        spacing: dp(8)

                        MDLabel:
                            id: detail_name
                            text: ""
                            font_style: "H5"
                            adaptive_height: True

                        MDSeparator:

                        MDLabel:
                            id: detail_age
                            text: ""
                            adaptive_height: True
                        MDLabel:
                            id: detail_phone
                            text: ""
                            adaptive_height: True
                        MDLabel:
                            id: detail_sub_date
                            text: ""
                            adaptive_height: True
                        MDLabel:
                            id: detail_period
                            text: ""
                            adaptive_height: True
                        MDLabel:
                            id: detail_expiry
                            text: ""
                            adaptive_height: True
                        MDLabel:
                            id: detail_status
                            text: ""
                            font_style: "H6"
                            adaptive_height: True
'''


class CustomerListItem(TwoLineAvatarIconListItem):
    customer_id = NumericProperty(0)
    status_icon = StringProperty("circle")
    status_color = (0.2, 0.7, 0.3, 1)


class HomeScreen(Screen):
    pass


class AddEditScreen(Screen):
    pass


class DetailScreen(Screen):
    pass


# Tab helper — KivyMD Tab requires a title attribute
from kivymd.uix.tab import MDTabsBase  # noqa: E402
from kivy.uix.floatlayout import FloatLayout  # noqa: E402


class Tab(FloatLayout, MDTabsBase):
    pass


class GymApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = None                 # created in on_start() after Android activity is ready
        self._editing_id = None        # None = add mode, int = edit mode
        self._current_customer = None  # for detail screen
        self._delete_dialog = None
        self._active_tab = "all"       # "all" | "active" | "expired"

    # ------------------------------------------------------------------
    # App lifecycle
    # ------------------------------------------------------------------

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)

    def on_start(self):
        try:
            self.db = Database()
            self.refresh_lists()
        except Exception as e:
            traceback.print_exc()
            Snackbar(text=f"DB Error: {e}").open()

    def on_stop(self):
        if self.db:
            self.db.close()

    # ------------------------------------------------------------------
    # Navigation helpers
    # ------------------------------------------------------------------

    def go_home(self):
        self.root.current = "home"
        self.refresh_lists()

    def go_add(self):
        self._editing_id = None
        self.clear_form()
        screen = self.root.get_screen("addedit")
        screen.ids.form_toolbar.title = "Add Customer"
        # Set today's date as default
        today = datetime.date.today().strftime("%Y-%m-%d")
        screen.ids.date_field.text = today
        screen.ids.period_field.text = "1"
        self._selected_period = 1
        self.root.current = "addedit"

    def go_edit(self):
        if self._current_customer is None:
            return
        c = self._current_customer
        self._editing_id = c["id"]
        screen = self.root.get_screen("addedit")
        screen.ids.form_toolbar.title = "Edit Customer"
        screen.ids.name_field.text = str(c["name"])
        screen.ids.age_field.text = str(c["age"])
        screen.ids.phone_field.text = str(c["phone"])
        screen.ids.date_field.text = str(c["subscription_date"])
        screen.ids.period_field.text = str(c["subscription_period"])
        self._selected_period = int(c["subscription_period"])
        self.root.current = "addedit"

    # ------------------------------------------------------------------
    # Date picker
    # ------------------------------------------------------------------

    def show_date_picker(self):
        screen = self.root.get_screen("addedit")
        current_text = screen.ids.date_field.text
        try:
            d = datetime.datetime.strptime(current_text, "%Y-%m-%d").date()
        except ValueError:
            d = datetime.date.today()
        picker = MDDatePicker(year=d.year, month=d.month, day=d.day)
        picker.bind(on_save=self._on_date_save, on_cancel=lambda *a: None)
        picker.open()

    def _on_date_save(self, instance, value, date_range):
        screen = self.root.get_screen("addedit")
        screen.ids.date_field.text = value.strftime("%Y-%m-%d")

    def set_period(self, months):
        self._selected_period = months
        screen = self.root.get_screen("addedit")
        screen.ids.period_field.text = str(months)

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def save_customer(self):
        screen = self.root.get_screen("addedit")
        name = screen.ids.name_field.text.strip()
        age_text = screen.ids.age_field.text.strip()
        phone = screen.ids.phone_field.text.strip()
        sub_date = screen.ids.date_field.text.strip()
        period_text = screen.ids.period_field.text.strip()

        # Validation
        if not name:
            Snackbar(text="Name is required!").open(); return
        if not age_text or not age_text.isdigit():
            Snackbar(text="Valid age is required!").open(); return
        if not phone:
            Snackbar(text="Phone number is required!").open(); return
        if not sub_date:
            Snackbar(text="Subscription date is required!").open(); return
        if not period_text or not period_text.isdigit():
            Snackbar(text="Select a subscription period!").open(); return

        age = int(age_text)
        period = int(period_text)

        if self._editing_id is None:
            result = self.db.add_customer(name, age, phone, sub_date, period)
            msg_ok = "Customer added successfully!"
        else:
            result = self.db.update_customer(self._editing_id, name, age, phone, sub_date, period)
            msg_ok = "Customer updated successfully!"

        if result is True:
            Snackbar(text=msg_ok).open()
            self.go_home()
        else:
            Snackbar(text=str(result)).open()

    def clear_form(self):
        screen = self.root.get_screen("addedit")
        screen.ids.name_field.text = ""
        screen.ids.age_field.text = ""
        screen.ids.phone_field.text = ""
        screen.ids.date_field.text = datetime.date.today().strftime("%Y-%m-%d")
        screen.ids.period_field.text = "1"
        self._selected_period = 1

    def confirm_delete(self, customer_id, customer_name):
        self._pending_delete_id = customer_id
        self._delete_dialog = MDDialog(
            title="Delete Customer",
            text=f"Delete [b]{customer_name}[/b]? This cannot be undone.",
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda *a: self._delete_dialog.dismiss()),
                MDRaisedButton(
                    text="DELETE",
                    md_bg_color=(0.9, 0.2, 0.2, 1),
                    on_release=lambda *a: self._do_delete(),
                ),
            ],
        )
        self._delete_dialog.open()

    def _do_delete(self):
        self._delete_dialog.dismiss()
        result = self.db.delete_customer(self._pending_delete_id)
        if result is True:
            Snackbar(text="Customer deleted.").open()
            self.refresh_lists()
        else:
            Snackbar(text=str(result)).open()

    # ------------------------------------------------------------------
    # List / search
    # ------------------------------------------------------------------

    def on_customer_tap(self, customer_id):
        customer = self.db.get_customer_by_id(customer_id)
        if not customer:
            return
        self._current_customer = customer
        self._show_detail(customer)
        self.root.current = "detail"

    def _show_detail(self, c):
        screen = self.root.get_screen("detail")
        is_active = self.db.check_subscription_status(c)
        expiry = self.db.get_expiry_date(c)
        ids = screen.ids
        ids.detail_name.text = c["name"]
        ids.detail_age.text = f"Age: {c['age']}"
        ids.detail_phone.text = f"Phone: {c['phone']}"
        ids.detail_sub_date.text = f"Start Date: {c['subscription_date']}"
        ids.detail_period.text = f"Period: {c['subscription_period']} month(s)"
        ids.detail_expiry.text = f"Expiry: {expiry}"
        ids.detail_status.text = "Status: ACTIVE" if is_active else "Status: EXPIRED"
        ids.detail_status.theme_text_color = "Custom"
        ids.detail_status.text_color = (0.2, 0.7, 0.3, 1) if is_active else (0.9, 0.2, 0.2, 1)

    def on_search(self, query):
        self.refresh_lists(query=query.strip().lower())

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        self._active_tab = tab_text.lower()

    def _get_export_dir(self):
        try:
            from android.storage import primary_external_storage_path
            path = os.path.join(primary_external_storage_path(), "Download")
        except ImportError:
            path = os.path.dirname(os.path.abspath(__file__))
        os.makedirs(path, exist_ok=True)
        return path

    def export_csv(self, mode):
        data_map = {
            "all": (self.db.get_all_customers, "all_customers"),
            "active": (self.db.get_active_subscriptions, "active_subscriptions"),
            "expired": (self.db.get_expired_subscriptions, "expired_subscriptions"),
        }
        getter, label = data_map[mode]
        customers = getter()
        if not customers:
            Snackbar(text="No data to export.").open()
            return
        timestamp = datetime.date.today().strftime("%Y%m%d")
        filename = f"{label}_{timestamp}.csv"
        filepath = os.path.join(self._get_export_dir(), filename)
        try:
            self.db.export_to_csv(filepath, customers)
            Snackbar(text=f"Saved: {filepath}", duration=4).open()
        except Exception as e:
            Snackbar(text=f"Export failed: {e}").open()

    def refresh_lists(self, query=""):
        all_customers = self.db.get_all_customers()
        screen = self.root.get_screen("home")
        ids = screen.ids

        def matches(c):
            if not query:
                return True
            return query in c["name"].lower() or query in str(c["phone"])

        for list_widget, customers in [
            (ids.list_all, all_customers),
            (ids.list_active, self.db.get_active_subscriptions()),
            (ids.list_expired, self.db.get_expired_subscriptions()),
        ]:
            list_widget.clear_widgets()
            for c in customers:
                if not matches(c):
                    continue
                is_active = self.db.check_subscription_status(c)
                expiry = self.db.get_expiry_date(c)
                item = CustomerListItem(
                    text=c["name"],
                    secondary_text=f"Phone: {c['phone']}  |  Expiry: {expiry}",
                    customer_id=c["id"],
                    status_icon="check-circle" if is_active else "alert-circle",
                    status_color=(0.2, 0.7, 0.3, 1) if is_active else (0.9, 0.2, 0.2, 1),
                )
                list_widget.add_widget(item)


if __name__ == "__main__":
    GymApp().run()
