from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.db.models.signal import Signal
from app.db.models.order import Order
from app.schemas.signal import SignalOut
from app.schemas.order import OrderOut, AcceptSignalRequest

router = APIRouter()


@router.get("/signals", summary="List signals", response_model=List[SignalOut])
def list_signals(db: Session = Depends(get_db)):
    signals = db.query(Signal).order_by(Signal.created_at.desc()).all()
    return signals


@router.post(
    "/signals/{signal_id}/accept",
    summary="Accept a signal and create an order",
    response_model=OrderOut,
)
def accept_signal(
    signal_id: int,
    payload: AcceptSignalRequest,
    db: Session = Depends(get_db),
):
    signal = db.query(Signal).filter(Signal.id == signal_id).first()
    if not signal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Signal not found")

    if signal.status == "accepted":
        raise HTTPException(status_code=400, detail="Signal already accepted")
    if signal.status == "rejected":
        raise HTTPException(status_code=400, detail="Signal already rejected")

    quantity = payload.quantity or 1.0  # فعلاً ساده

    order = Order(
        signal_id=signal.id,
        symbol=signal.symbol,
        market=signal.market,
        direction=signal.direction,
        entry=signal.entry,
        sl=signal.sl,
        tp=signal.tp,
        quantity=quantity,
        status="pending",   # در آینده: بعد از اجرای واقعی سفارش، open/closed می‌شه
    )
    db.add(order)

    signal.status = "accepted"
    db.add(signal)

    db.commit()
    db.refresh(order)

    return order


@router.post(
    "/signals/{signal_id}/reject",
    summary="Reject a signal",
    response_model=SignalOut,
)
def reject_signal(
    signal_id: int,
    db: Session = Depends(get_db),
):
    signal = db.query(Signal).filter(Signal.id == signal_id).first()
    if not signal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Signal not found")

    if signal.status == "accepted":
        raise HTTPException(status_code=400, detail="Signal already accepted")
    if signal.status == "rejected":
        raise HTTPException(status_code=400, detail="Signal already rejected")

    signal.status = "rejected"
    db.add(signal)
    db.commit()
    db.refresh(signal)
    return signal
