from dataclasses import dataclass, field
from typing import List, Optional, Literal, Dict


@dataclass
class BookingOption:
    title: str
    app: str
    price: int
    option_id: str


@dataclass
class SelectedOption:
    title: str
    app: str
    option_id: str


@dataclass
class BookingResult:
    status: Literal["success", "failed"]
    waiting_time: int

@dataclass
class LoginInfo:
    phone_number: str
    otp: str


@dataclass
class TransportBookingData:
    pickup_location: Optional[str] = None  # e.g. "current_location" or address
    destination: Optional[str] = None
    time: Optional[str] = "now"  # Future support
    app: Optional[str] = None  # "grab", "gojek", etc.
    is_logged_in: bool = True
    login_info: Optional[LoginInfo] = None
    is_payment_default_exist: bool = True  # "cash", "wallet", etc.
    confirmation_check_done: bool = False
    booking_options: List[BookingOption] = field(default_factory=list)
    selected_option: Optional[SelectedOption] = None
    booking_result: Optional[BookingResult] = None
    cancelled: bool = False


@dataclass
class FlowState:
    flow: Literal["transport_booking"]
    step: Literal[
        "start",
        "awaiting_missing_info",
        "login",
        "login_otp_pending"
        "confirmation_check_pending",
        "awaiting_user_confirmation",
        "booking_in_progress",
        "handle_waiting_time",
        "cancel_and_restart",
        "done"
    ]
    data: TransportBookingData


def parse_booking_options(raw_list):
    return [BookingOption(**opt) for opt in raw_list]

def parse_selected_option(raw):
    return SelectedOption(**raw) if raw else None

def parse_booking_result(raw):
    return BookingResult(**raw) if raw else None

def parse_login_info(raw):
    return LoginInfo(**raw) if raw else None

def fetch_rides(rides):
    booking_options = []
    for i, opt in enumerate(rides):
        booking_options.append(
            BookingOption(
                title=opt["title"],
                app="grab",
                price=opt["price"],
                option_id=f"{opt['title'].lower().replace(' ', '')}-grab-{i:03}"
            )
        )
    return booking_options