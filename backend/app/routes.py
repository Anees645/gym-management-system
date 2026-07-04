from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select, Session
from app.database import get_session
from app.models import (
    Users,
    userCreation,
    Members,
    memberCreation,
    Trainers,
    trainerCreation,
    membershipPlans,
    membershipPlansCreation,
    Memberships,
    membershipsCreation,
    Attendance,
    attendanceRecord,
    Payments,
    paymentsRecord,
    WorkoutPlans,
    workoutPlansCreation,
    DietPlans,
    dietPlansGuide,
    Exercises,
    exercisesGuide,
    WorkoutExercises,
    workoutExercisesPlan,
    Equipment,
    equipmentsInfo,
    Maintenance,
    maintenanceRecords,
    ProgressLogs,
    progressLogsHandling,
    AnnouncementDetails,
)
from typing import Annotated

SessionDep = Annotated[Session, Depends(get_session)]

api_router = APIRouter()


@api_router.post("/users/", response_model=Users, status_code=201, tags=["Users"])
def create_user(user_in: userCreation, session: SessionDep):
    existing = session.exec(select(Users).where(Users.email == user_in.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists.")
    db_user = Users.model_validate(user_in)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@api_router.get("/users/", response_model=list[Users], tags=["Users"])
def read_all_users(session: SessionDep):
    return session.exec(select(Users)).all()


@api_router.put("/users/{user_id}", response_model=Users, tags=["Users"])
def update_user(user_id: int, user_in: userCreation, session: SessionDep):
    db_user = session.get(Users, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user_in.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@api_router.delete("/users/{user_id}", tags=["Users"])
def delete_user(user_id: int, session: SessionDep):
    db_user = session.get(Users, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(db_user)
    session.commit()
    return {"status": "success", "message": "User deleted"}


@api_router.post("/members/", response_model=Members, status_code=201, tags=["Members"])
def create_member_profile(member_in: memberCreation, session: SessionDep):
    user = session.get(Users, member_in.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User account not found.")
    existing_profile = session.exec(
        select(Members).where(Members.user_id == member_in.user_id)
    ).first()
    if existing_profile:
        raise HTTPException(
            status_code=400, detail="Profile already exists for this user_id."
        )
    db_member = Members.model_validate(member_in)
    session.add(db_member)
    session.commit()
    session.refresh(db_member)
    return db_member


@api_router.get("/members/", response_model=list[Members], tags=["Members"])
def read_all_members(session: SessionDep):
    return session.exec(select(Members)).all()


@api_router.put("/members/{member_id}", response_model=Members, tags=["Members"])
def update_member_profile(
    member_id: int, member_in: memberCreation, session: SessionDep
):
    db_member = session.get(Members, member_id)
    if not db_member:
        raise HTTPException(status_code=404, detail="Member profile not found")

    member_data = member_in.model_dump(exclude_unset=True)
    for key, value in member_data.items():
        setattr(db_member, key, value)

    session.add(db_member)
    session.commit()
    session.refresh(db_member)
    return db_member


@api_router.delete("/members/{member_id}", tags=["Members"])
def delete_member_profile(member_id: int, session: SessionDep):
    db_member = session.get(Members, member_id)
    if not db_member:
        raise HTTPException(status_code=404, detail="Member profile not found")
    session.delete(db_member)
    session.commit()
    return {"status": "success", "message": "Member profile deleted"}


@api_router.post(
    "/trainers/", response_model=Trainers, status_code=201, tags=["Trainers"]
)
def create_trainer_profile(trainer_in: trainerCreation, session: SessionDep):
    user = session.get(Users, trainer_in.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User account not found.")

    existing_profile = session.exec(
        select(Trainers).where(Trainers.user_id == trainer_in.user_id)
    ).first()
    if existing_profile:
        raise HTTPException(
            status_code=400, detail="Trainer profile already exists for this user_id."
        )

    db_trainer = Trainers.model_validate(trainer_in)
    session.add(db_trainer)
    session.commit()
    session.refresh(db_trainer)
    return db_trainer


@api_router.get("/trainers/", response_model=list[Trainers], tags=["Trainers"])
def read_all_trainers(session: SessionDep):
    return session.exec(select(Trainers)).all()


@api_router.put("/trainers/{id}", response_model=Trainers, tags=["Trainers"])
def update_trainer_profile(id: int, trainer_in: dict, session: SessionDep):
    db_trainer = session.get(Trainers, id)
    if not db_trainer:
        raise HTTPException(status_code=404, detail="Trainer profile not found")

    for key, value in trainer_in.items():
        if key == "user_id" or key == "id":
            continue  # Keep immutable identifier keys safe
        if hasattr(db_trainer, key):
            setattr(db_trainer, key, value)

    session.add(db_trainer)
    session.commit()
    session.refresh(db_trainer)
    return db_trainer


@api_router.delete("/trainers/{id}", tags=["Trainers"])
def delete_trainer_profile(id: int, session: SessionDep):
    db_trainer = session.get(Trainers, id)
    if not db_trainer:
        raise HTTPException(status_code=404, detail="Trainer profile not found")

    session.delete(db_trainer)
    session.commit()
    return {"status": "success", "message": "Trainer profile successfully deleted"}


@api_router.post(
    "/plans/", response_model=membershipPlans, status_code=201, tags=["Plans"]
)
def create_membership_plan(plan_in: membershipPlansCreation, session: SessionDep):
    db_plan = membershipPlans.model_validate(plan_in)
    session.add(db_plan)
    session.commit()
    session.refresh(db_plan)
    return db_plan


@api_router.get("/plans/", response_model=list[membershipPlans], tags=["Plans"])
def read_all_plans(session: SessionDep):
    return session.exec(select(membershipPlans)).all()


@api_router.put("/plans/{plan_id}", response_model=membershipPlans, tags=["Plans"])
def update_membership_plan(
    plan_id: int, plan_in: membershipPlansCreation, session: SessionDep
):
    db_plan = session.get(membershipPlans, plan_id)
    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    plan_data = plan_in.model_dump(exclude_unset=True)
    for key, value in plan_data.items():
        setattr(db_plan, key, value)

    session.add(db_plan)
    session.commit()
    session.refresh(db_plan)
    return db_plan


@api_router.delete("/plans/{plan_id}", tags=["Plans"])
def delete_membership_plan(plan_id: int, session: SessionDep):
    db_plan = session.get(membershipPlans, plan_id)
    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    session.delete(db_plan)
    session.commit()
    return {"status": "success", "message": "Plan deleted"}


@api_router.post(
    "/memberships/", response_model=Memberships, status_code=201, tags=["Memberships"]
)
def contract_membership(membership_in: membershipsCreation, session: SessionDep):
    member = session.get(Members, membership_in.member_id)
    plan = session.get(membershipPlans, membership_in.plan_id)
    if not member or not plan:
        raise HTTPException(
            status_code=404, detail="Member or Membership Plan not found."
        )
    db_membership = Memberships.model_validate(membership_in)
    session.add(db_membership)
    session.commit()
    session.refresh(db_membership)
    return db_membership


@api_router.get("/memberships/", response_model=list[Memberships], tags=["Memberships"])
def read_all_memberships(session: SessionDep):
    return session.exec(select(Memberships)).all()


@api_router.put("/memberships/{id}", response_model=Memberships, tags=["Memberships"])
def update_membership(id: int, membership_in: dict, session: SessionDep):
    db_membership = session.get(Memberships, id)
    if not db_membership:
        raise HTTPException(status_code=404, detail="Membership contract not found")

    for key, value in membership_in.items():
        if key == "id":
            continue
        if hasattr(db_membership, key):
            setattr(db_membership, key, value)

    session.add(db_membership)
    session.commit()
    session.refresh(db_membership)
    return db_membership


@api_router.delete("/memberships/{id}", tags=["Memberships"])
def delete_membership(id: int, session: SessionDep):
    db_membership = session.get(Memberships, id)
    if not db_membership:
        raise HTTPException(status_code=404, detail="Membership contract not found")
    session.delete(db_membership)
    session.commit()
    return {"status": "success", "message": "Membership contract deleted"}


@api_router.post(
    "/attendance/", response_model=Attendance, status_code=201, tags=["Attendance"]
)
def log_attendance(attendance_in: attendanceRecord, session: SessionDep):
    member = session.get(Members, attendance_in.member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found.")
    db_attendance = Attendance.model_validate(attendance_in)
    session.add(db_attendance)
    session.commit()
    session.refresh(db_attendance)
    return db_attendance


@api_router.get("/attendance/", response_model=list[Attendance], tags=["Attendance"])
def read_all_attendance(session: SessionDep):
    return session.exec(select(Attendance)).all()


@api_router.put("/attendance/{id}", response_model=Attendance, tags=["Attendance"])
def update_attendance(id: int, attendance_in: dict, session: SessionDep):
    db_attendance = session.get(Attendance, id)
    if not db_attendance:
        raise HTTPException(status_code=404, detail="Attendance record not found")

    for key, value in attendance_in.items():
        if key == "id":
            continue
        if hasattr(db_attendance, key):
            setattr(db_attendance, key, value)

    session.add(db_attendance)
    session.commit()
    session.refresh(db_attendance)
    return db_attendance


@api_router.delete("/attendance/{id}", tags=["Attendance"])
def delete_attendance(id: int, session: SessionDep):
    db_attendance = session.get(Attendance, id)
    if not db_attendance:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    session.delete(db_attendance)
    session.commit()
    return {"status": "success", "message": "Attendance record deleted"}


@api_router.post(
    "/payments/", response_model=Payments, status_code=201, tags=["Payments"]
)
def process_payment(payment_in: paymentsRecord, session: SessionDep):
    membership = session.get(Memberships, payment_in.membership_id)
    if not membership:
        raise HTTPException(
            status_code=404, detail="Membership contract reference not found."
        )
    db_payment = Payments.model_validate(payment_in)
    session.add(db_payment)
    session.commit()
    session.refresh(db_payment)
    return db_payment


@api_router.get("/payments/", response_model=list[Payments], tags=["Payments"])
def read_all_payments(session: SessionDep):
    return session.exec(select(Payments)).all()


@api_router.put("/payments/{id}", response_model=Payments, tags=["Payments"])
def update_payment(id: int, payment_in: dict, session: SessionDep):
    db_payment = session.get(Payments, id)
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment record not found")

    for key, value in payment_in.items():
        if key == "id":
            continue
        if hasattr(db_payment, key):
            setattr(db_payment, key, value)

    session.add(db_payment)
    session.commit()
    session.refresh(db_payment)
    return db_payment


@api_router.delete("/payments/{id}", tags=["Payments"])
def delete_payment(id: int, session: SessionDep):
    db_payment = session.get(Payments, id)
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment record not found")
    session.delete(db_payment)
    session.commit()
    return {"status": "success", "message": "Payment record deleted"}


# workout endpoints


@api_router.post(
    "/workout-plans/",
    response_model=WorkoutPlans,
    status_code=201,
    tags=["Workout Plans"],
)
def create_workout_plan(plan_in: workoutPlansCreation, session: SessionDep):
    db_plan = WorkoutPlans.model_validate(plan_in)
    try:
        session.add(db_plan)
        session.commit()
        session.refresh(db_plan)
        return db_plan
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Database Error: {str(e)}")


@api_router.get(
    "/workout-plans/", response_model=list[WorkoutPlans], tags=["Workout Plans"]
)
def read_all_workout_plans(session: SessionDep):
    return session.exec(select(WorkoutPlans)).all()


@api_router.put(
    "/workout-plans/{id}", response_model=WorkoutPlans, tags=["Workout Plans"]
)
def update_workout_plan(id: int, plan_in: dict, session: SessionDep):
    db_plan = session.get(WorkoutPlans, id)
    if not db_plan:
        raise HTTPException(status_code=404, detail="Workout plan not found")

    for key, value in plan_in.items():
        if key == "id":
            continue
        if hasattr(db_plan, key):
            setattr(db_plan, key, value)

    session.add(db_plan)
    session.commit()
    session.refresh(db_plan)
    return db_plan


@api_router.delete("/workout-plans/{id}", tags=["Workout Plans"])
def delete_workout_plan(id: int, session: SessionDep):
    db_plan = session.get(WorkoutPlans, id)
    if not db_plan:
        raise HTTPException(status_code=404, detail="Workout plan not found")

    session.delete(db_plan)
    session.commit()
    return {"status": "success", "message": "Workout plan successfully deleted"}


@api_router.post(
    "/diet-plans/", response_model=DietPlans, status_code=201, tags=["Diet Plans"]
)
def create_diet_plan(diet_in: dietPlansGuide, session: SessionDep):
    trainer = session.get(Trainers, diet_in.trainer_id)
    member = session.get(Members, diet_in.member_id)
    if not trainer or not member:
        raise HTTPException(status_code=404, detail="Trainer or Member not found.")
    db_diet = DietPlans.model_validate(diet_in)
    session.add(db_diet)
    session.commit()
    session.refresh(db_diet)
    return db_diet


@api_router.get("/diet-plans/", response_model=list[DietPlans], tags=["Diet Plans"])
def read_all_diet_plans(session: SessionDep):
    return session.exec(select(DietPlans)).all()


@api_router.put("/diet-plans/{id}", response_model=DietPlans, tags=["Diet Plans"])
def update_diet_plan(id: int, diet_in: dict, session: SessionDep):
    db_diet = session.get(DietPlans, id)
    if not db_diet:
        raise HTTPException(status_code=404, detail="Diet plan not found")

    for key, value in diet_in.items():
        if key == "id":
            continue
        if hasattr(db_diet, key):
            setattr(db_diet, key, value)

    session.add(db_diet)
    session.commit()
    session.refresh(db_diet)
    return db_diet


@api_router.delete("/diet-plans/{id}", tags=["Diet Plans"])
def delete_diet_plan(id: int, session: SessionDep):
    db_diet = session.get(DietPlans, id)
    if not db_diet:
        raise HTTPException(status_code=404, detail="Diet plan not found")
    session.delete(db_diet)
    session.commit()
    return {"status": "success", "message": "Diet plan deleted"}


# exercises ...
@api_router.post(
    "/exercises/",
    response_model=Exercises,
    status_code=201,
    tags=["Workout Routines & Exercises"],
)
def add_exercise_to_bank(exercise_in: exercisesGuide, session: SessionDep):
    db_exercise = Exercises.model_validate(exercise_in)
    session.add(db_exercise)
    session.commit()
    session.refresh(db_exercise)
    return db_exercise


@api_router.put(
    "/exercises/{id}",
    response_model=Exercises,
    tags=["Workout Routines & Exercises"],
)
def update_exercise(id: int, exercise_in: dict, session: SessionDep):
    db_exercise = session.get(Exercises, id)
    if not db_exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    for key, value in exercise_in.items():
        if key == "id":
            continue
        if hasattr(db_exercise, key):
            setattr(db_exercise, key, value)

    session.add(db_exercise)
    session.commit()
    session.refresh(db_exercise)
    return db_exercise


@api_router.delete("/exercises/{id}", tags=["Workout Routines & Exercises"])
def delete_exercise(id: int, session: SessionDep):
    db_exercise = session.get(Exercises, id)
    if not db_exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    session.delete(db_exercise)
    session.commit()
    return {"status": "success", "message": "Exercise deleted"}


@api_router.post(
    "/workout-exercises/",
    response_model=WorkoutExercises,
    status_code=201,
    tags=["Workout Routines & Exercises"],
)
def link_exercise_to_plan(link_in: workoutExercisesPlan, session: SessionDep):
    """Link an exercise to a specific workout routine with set/rep assignments."""
    plan = session.get(WorkoutPlans, link_in.workout_plan_id)
    exercise = session.get(Exercises, link_in.exercise_id)
    if not plan or not exercise:
        raise HTTPException(
            status_code=404, detail="Workout Plan or Exercise not found."
        )
    db_link = WorkoutExercises.model_validate(link_in)
    session.add(db_link)
    session.commit()
    session.refresh(db_link)
    return db_link


@api_router.put(
    "/workout-exercises/{id}",
    response_model=WorkoutExercises,
    tags=["Workout Routines & Exercises"],
)
def update_workout_exercise_link(id: int, link_in: dict, session: SessionDep):
    db_link = session.get(WorkoutExercises, id)
    if not db_link:
        raise HTTPException(status_code=404, detail="Workout-exercise link not found")

    for key, value in link_in.items():
        if key == "id":
            continue
        if hasattr(db_link, key):
            setattr(db_link, key, value)

    session.add(db_link)
    session.commit()
    session.refresh(db_link)
    return db_link


@api_router.delete("/workout-exercises/{id}", tags=["Workout Routines & Exercises"])
def delete_workout_exercise_link(id: int, session: SessionDep):
    db_link = session.get(WorkoutExercises, id)
    if not db_link:
        raise HTTPException(status_code=404, detail="Workout-exercise link not found")
    session.delete(db_link)
    session.commit()
    return {"status": "success", "message": "Workout-exercise link deleted"}


# maintenance , equipment ...
@api_router.post(
    "/equipment/",
    response_model=Equipment,
    status_code=201,
    tags=["Inventory & Maintenance"],
)
def catalog_equipment(equip_in: equipmentsInfo, session: SessionDep):
    """Log gym infrastructure/machinery items (e.g., Treadmill, Cable Crossover)."""
    db_equip = Equipment.model_validate(equip_in)
    session.add(db_equip)
    session.commit()
    session.refresh(db_equip)
    return db_equip


@api_router.get(
    "/equipment/", response_model=list[Equipment], tags=["Inventory & Maintenance"]
)
def read_all_equipment(session: SessionDep):
    return session.exec(select(Equipment)).all()


@api_router.put(
    "/equipment/{id}", response_model=Equipment, tags=["Inventory & Maintenance"]
)
def update_equipment(id: int, equip_in: dict, session: SessionDep):
    db_equip = session.get(Equipment, id)
    if not db_equip:
        raise HTTPException(status_code=404, detail="Equipment item not found")

    for key, value in equip_in.items():
        if key == "id":
            continue
        if hasattr(db_equip, key):
            setattr(db_equip, key, value)

    session.add(db_equip)
    session.commit()
    session.refresh(db_equip)
    return db_equip


@api_router.delete("/equipment/{id}", tags=["Inventory & Maintenance"])
def delete_equipment(id: int, session: SessionDep):
    db_equip = session.get(Equipment, id)
    if not db_equip:
        raise HTTPException(status_code=404, detail="Equipment item not found")
    session.delete(db_equip)
    session.commit()
    return {"status": "success", "message": "Equipment item deleted"}


@api_router.post(
    "/maintenance/",
    response_model=Maintenance,
    status_code=201,
    tags=["Inventory & Maintenance"],
)
def log_maintenance_ticket(repair_in: maintenanceRecords, session: SessionDep):
    equip = session.get(Equipment, repair_in.equipment_id)
    if not equip:
        raise HTTPException(status_code=404, detail="Equipment item not found.")
    db_repair = Maintenance.model_validate(repair_in)
    session.add(db_repair)
    session.commit()
    session.refresh(db_repair)
    return db_repair


@api_router.get(
    "/maintenance/", response_model=list[Maintenance], tags=["Inventory & Maintenance"]
)
def read_all_maintenance(session: SessionDep):
    return session.exec(select(Maintenance)).all()


@api_router.put(
    "/maintenance/{id}", response_model=Maintenance, tags=["Inventory & Maintenance"]
)
def update_maintenance(id: int, repair_in: dict, session: SessionDep):
    db_repair = session.get(Maintenance, id)
    if not db_repair:
        raise HTTPException(status_code=404, detail="Maintenance record not found")

    for key, value in repair_in.items():
        if key == "id":
            continue
        if hasattr(db_repair, key):
            setattr(db_repair, key, value)

    session.add(db_repair)
    session.commit()
    session.refresh(db_repair)
    return db_repair


@api_router.delete("/maintenance/{id}", tags=["Inventory & Maintenance"])
def delete_maintenance(id: int, session: SessionDep):
    db_repair = session.get(Maintenance, id)
    if not db_repair:
        raise HTTPException(status_code=404, detail="Maintenance record not found")
    session.delete(db_repair)
    session.commit()
    return {"status": "success", "message": "Maintenance record deleted"}


# progress endpoints
@api_router.post(
    "/progress-logs/",
    response_model=ProgressLogs,
    status_code=201,
    tags=["Progress Tracking"],
)
def record_biometrics(log_in: progressLogsHandling, session: SessionDep):
    member = session.get(Members, log_in.member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member profile not found.")
    db_log = ProgressLogs.model_validate(log_in)
    session.add(db_log)
    session.commit()
    session.refresh(db_log)
    return db_log


@api_router.get(
    "/progress-logs/",
    response_model=list[ProgressLogs],
    tags=["Progress Tracking"],
)
def get_all_biometrics(session: SessionDep):
    return session.exec(select(ProgressLogs)).all()


@api_router.get(
    "/progress-logs/{member_id}",
    response_model=list[ProgressLogs],
    tags=["Progress Tracking"],
)
def get_member_biometrics_history(member_id: int, session: SessionDep):
    return session.exec(
        select(ProgressLogs).where(ProgressLogs.member_id == member_id)
    ).all()


@api_router.put(
    "/progress-logs/{id}",
    response_model=ProgressLogs,
    tags=["Progress Tracking"],
)
def update_progress_log(id: int, log_in: dict, session: SessionDep):
    db_log = session.get(ProgressLogs, id)
    if not db_log:
        raise HTTPException(status_code=404, detail="Progress log entry not found")

    for key, value in log_in.items():
        if key == "id":
            continue
        if hasattr(db_log, key):
            setattr(db_log, key, value)

    session.add(db_log)
    session.commit()
    session.refresh(db_log)
    return db_log


@api_router.delete("/progress-logs/{id}", tags=["Progress Tracking"])
def delete_progress_log(id: int, session: SessionDep):
    db_log = session.get(ProgressLogs, id)
    if not db_log:
        raise HTTPException(status_code=404, detail="Progress log entry not found")
    session.delete(db_log)
    session.commit()
    return {"status": "success", "message": "Progress log entry deleted"}


# announcement endpoints
@api_router.post(
    "/announcements/",
    response_model=AnnouncementDetails,
    status_code=201,
    tags=["Announcements"],
)
def broadcast_announcement(announcement_in: AnnouncementDetails, session: SessionDep):
    session.add(announcement_in)
    session.commit()
    session.refresh(announcement_in)
    return announcement_in


@api_router.get(
    "/announcements/", response_model=list[AnnouncementDetails], tags=["Announcements"]
)
def get_all_announcements(session: SessionDep):
    return session.exec(
        select(AnnouncementDetails).order_by(AnnouncementDetails.created_at.desc())
    ).all()


@api_router.put(
    "/announcements/{id}",
    response_model=AnnouncementDetails,
    tags=["Announcements"],
)
def update_announcement(id: int, announcement_in: dict, session: SessionDep):
    db_announcement = session.get(AnnouncementDetails, id)
    if not db_announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    for key, value in announcement_in.items():
        if key in ("id", "created_at"):
            continue
        if hasattr(db_announcement, key):
            setattr(db_announcement, key, value)

    session.add(db_announcement)
    session.commit()
    session.refresh(db_announcement)
    return db_announcement


@api_router.delete("/announcements/{id}", tags=["Announcements"])
def delete_announcement(id: int, session: SessionDep):
    db_announcement = session.get(AnnouncementDetails, id)
    if not db_announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    session.delete(db_announcement)
    session.commit()
    return {"status": "success", "message": "Announcement deleted"}
