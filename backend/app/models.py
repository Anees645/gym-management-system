from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from sqlalchemy import Text, Numeric
from decimal import Decimal


class userCreation(SQLModel):
    name: str | None = Field(default=None, unique=True, max_length=50)
    email: str = Field(default=None, max_length=100, unique=True, nullable=False)
    password: str = Field(max_length=50)
    role: str = Field(max_length=20)
    created_at: datetime = Field(default_factory=datetime.now)


class Users(userCreation, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    member: "Members" = Relationship(back_populates="user")
    trainer: "Trainers" = Relationship(back_populates="user")


# many to many bridge (imp)


class trainerAndMember(SQLModel):
    trainer_id: int = Field(foreign_key="trainers.id", primary_key=True)
    member_id: int = Field(foreign_key="members.id", primary_key=True)
    assign_date: datetime = Field(default_factory=datetime.now)


class TrainerMember(trainerAndMember, table=True):
    __tablename__ = "trainer_member"


class memberCreation(SQLModel):
    user_id: int = Field(foreign_key="users.id", unique=True)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    gender: str = Field(max_length=10)
    dob: datetime
    address: str = Field(sa_type=Text)


class Members(memberCreation, table=True):
    __tablename__ = "members"
    id: int | None = Field(default=None, primary_key=True)
    user: Users = Relationship(back_populates="member")
    memberships: list["Memberships"] = Relationship(back_populates="member")
    attendance: list["Attendance"] = Relationship(back_populates="member")
    workout_plans: list["WorkoutPlans"] = Relationship(back_populates="member")
    diet_plans: list["DietPlans"] = Relationship(back_populates="member")
    progress_logs: list["ProgressLogs"] = Relationship(back_populates="member")
    trainers: list["Trainers"] = Relationship(
        back_populates="members", link_model=TrainerMember
    )


class trainerCreation(SQLModel):
    user_id: int = Field(foreign_key="users.id", unique=True)
    specialization: str | None = Field(max_length=100, default=None)
    experience: int = Field(ge=3)
    salary: Decimal = Field(sa_type=Numeric(10, 2))


class Trainers(trainerCreation, table=True):
    __tablename__ = "trainers"
    id: int | None = Field(default=None, primary_key=True)
    user: Users = Relationship(back_populates="trainer")
    workout_plans: list["WorkoutPlans"] = Relationship(back_populates="trainer")
    diet_plans: list["DietPlans"] = Relationship(back_populates="trainer")
    members: list["Members"] = Relationship(
        back_populates="trainers", link_model=TrainerMember
    )


class membershipPlansCreation(SQLModel):
    name: str = Field(max_length=50)
    duration_months: int
    price: Decimal = Field(sa_type=Numeric(10, 2))
    description: str | None = Field(sa_type=Text, default=None)


class membershipPlans(membershipPlansCreation, table=True):
    __tablename__ = "membership_plans"
    id: int | None = Field(default=None, primary_key=True)
    memberships: list["Memberships"] = Relationship(back_populates="plan")


class membershipsCreation(SQLModel):
    member_id: int = Field(foreign_key="members.id")
    plan_id: int = Field(foreign_key="membership_plans.id")
    start_date: datetime
    end_date: datetime
    status: str | None = Field(default=None, max_length=20)


class Memberships(membershipsCreation, table=True):
    __tablename__ = "memberships"
    id: int | None = Field(default=None, primary_key=True)
    member: Members = Relationship(back_populates="memberships")
    plan: membershipPlans = Relationship(back_populates="memberships")
    payments: list["Payments"] = Relationship(back_populates="membership")


class paymentsRecord(SQLModel):
    membership_id: int = Field(foreign_key="memberships.id")
    amount: Decimal = Field(sa_type=Numeric(10, 2))
    payment_date: datetime
    payment_method: str = Field(max_length=30)
    status: str = Field(max_length=20)


class Payments(paymentsRecord, table=True):
    __tablename__ = "payments"
    id: int | None = Field(default=None, primary_key=True)
    membership: Memberships = Relationship(back_populates="payments")


class attendanceRecord(SQLModel):
    member_id: int = Field(foreign_key="members.id")
    check_in: datetime
    check_out: datetime | None = None


class Attendance(attendanceRecord, table=True):
    __tablename__ = "attendance"
    id: int | None = Field(default=None, primary_key=True)
    member: Members = Relationship(back_populates="attendance")


class workoutPlansCreation(SQLModel):
    trainer_id: int = Field(foreign_key="trainers.id")
    member_id: int = Field(foreign_key="members.id")
    title: str = Field(max_length=100)
    description: str | None = Field(sa_type=Text, default=None)


class WorkoutPlans(workoutPlansCreation, table=True):
    __tablename__ = "workout_plans"
    id: int | None = Field(default=None, primary_key=True)
    trainer: Trainers = Relationship(back_populates="workout_plans")
    member: Members = Relationship(back_populates="workout_plans")
    exercises: list["WorkoutExercises"] = Relationship(back_populates="workout_plan")


class exercisesGuide(SQLModel):
    name: str = Field(max_length=100)
    muscle_group: str = Field(max_length=50)
    difficulty: str = Field(max_length=20)
    description: str | None = Field(sa_type=Text, default=None)


class Exercises(exercisesGuide, table=True):
    __tablename__ = "exercises"
    id: int | None = Field(default=None, primary_key=True)
    workout_plans: list["WorkoutExercises"] = Relationship(back_populates="exercise")


class workoutExercisesPlan(SQLModel):
    workout_plan_id: int = Field(foreign_key="workout_plans.id")
    exercise_id: int = Field(foreign_key="exercises.id")
    sets: int
    reps: int
    rest_time: int


class WorkoutExercises(workoutExercisesPlan, table=True):
    __tablename__ = "workout_exercises"
    id: int | None = Field(default=None, primary_key=True)
    workout_plan: WorkoutPlans = Relationship(back_populates="exercises")
    exercise: Exercises = Relationship(back_populates="workout_plans")


class dietPlansGuide(SQLModel):
    trainer_id: int = Field(foreign_key="trainers.id")
    member_id: int = Field(foreign_key="members.id")
    title: str = Field(max_length=100)
    calories: int
    notes: str | None = Field(sa_type=Text, default=None)


class DietPlans(dietPlansGuide, table=True):
    __tablename__ = "diet_plans"
    id: int | None = Field(default=None, primary_key=True)
    trainer: Trainers = Relationship(back_populates="diet_plans")
    member: Members = Relationship(back_populates="diet_plans")


class equipmentsInfo(SQLModel):
    name: str = Field(max_length=100)
    purchase_date: datetime
    condition: str = Field(max_length=20)
    location: str = Field(max_length=50)


class Equipment(equipmentsInfo, table=True):
    __tablename__ = "equipment"
    id: int | None = Field(default=None, primary_key=True)
    maintenance_records: list["Maintenance"] = Relationship(back_populates="equipment")


class maintenanceRecords(SQLModel):
    equipment_id: int = Field(foreign_key="equipment.id")
    maintenance_date: datetime
    description: str = Field(sa_type=Text)
    cost: Decimal = Field(sa_type=Numeric(10, 2))


class Maintenance(maintenanceRecords, table=True):
    __tablename__ = "maintenance"
    id: int | None = Field(default=None, primary_key=True)
    equipment: Equipment = Relationship(back_populates="maintenance_records")


class progressLogsHandling(SQLModel):
    member_id: int = Field(foreign_key="members.id")
    weight: Decimal = Field(sa_type=Numeric(5, 2))
    body_fat: Decimal | None = Field(sa_type=Numeric(5, 2), default=None)
    chest: Decimal | None = Field(sa_type=Numeric(5, 2), default=None)
    waist: Decimal | None = Field(sa_type=Numeric(5, 2), default=None)
    arms: Decimal | None = Field(sa_type=Numeric(5, 2), default=None)
    date: datetime


class ProgressLogs(progressLogsHandling, table=True):
    __tablename__ = "progress_logs"
    id: int | None = Field(default=None, primary_key=True)
    member: Members = Relationship(back_populates="progress_logs")


class AnnouncementDetails(SQLModel, table=True):
    __tablename__ = "announcements"
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=100)
    description: str = Field(sa_type=Text)
    created_at: datetime = Field(default_factory=datetime.now)
