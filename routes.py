import datetime
import uuid
from flask import Blueprint, current_app, render_template, request, redirect, url_for


pages = Blueprint("habits", __name__, template_folder="templates", static_folder="static")


@pages.context_processor
def add_calc_date_range():
    def date_range(start: datetime.datetime):
        dates = [start + datetime.timedelta(days=diff) for diff in range(-3, 4)]
        return dates
    return {"date_range": date_range}


@pages.route("/fizzbuzz")
def todo():
    return render_template("fizzbuzz.html")


def today_at_midnight():
    today = datetime.datetime.today()
    return today.replace(hour=0, minute=0, second=0, microsecond=0)


@pages.route("/")
def index():
    date_str = request.args.get("date")
    if date_str:
        selected_date = datetime.datetime.fromisoformat(date_str).date()
    else:
        selected_date = datetime.datetime.today().date()

    start_of_day = datetime.datetime.combine(selected_date, datetime.time.min)
    end_of_day = datetime.datetime.combine(selected_date, datetime.time.max)
    
    habits_on_date = current_app.db.habits.find({
        "added": {"$gte": start_of_day, "$lte": end_of_day}
    })
    
    completions = [
        habit["habit"]
        for habit in current_app.db.completions.find({"date": start_of_day.strftime("%Y-%m-%d")})
    ]
    
    return render_template(
        "index.html",
        habits=habits_on_date,
        selected_date=selected_date,
        completions=completions,
        title="Habit Tracker - Home",
    )




@pages.route("/add", methods=["GET", "POST"])
def add_habit():
    if request.method == "POST":
        habit_name = request.form.get("habit")
        selected_date_str = request.args.get("date")

        if selected_date_str:
            selected_date = datetime.datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        else:
            selected_date = datetime.datetime.today().date()

        current_app.db.habits.insert_one(
            {"_id": uuid.uuid4().hex, "added": datetime.datetime.combine(selected_date, datetime.datetime.min.time()), "name": habit_name}
        )


        return redirect(url_for(".index", date=selected_date_str))

    today = today_at_midnight()

    return render_template(
        "add_habit.html",
        title="Habit Tracker - Add Habit",
        selected_date=today,
    )

       
@pages.route("/complete", methods=["POST"])
def complete():
    date_string = request.form.get("date")
    habit_id = request.form.get("habitId")
    date = datetime.datetime.fromisoformat(date_string).date()
    
    # Converter a data para uma representação de string
    date_str = date.strftime("%Y-%m-%d")
    
    current_app.db.completions.insert_one({"date": date_str, "habit": habit_id})

    # Atualize a tarefa como concluída no banco de dados
    current_app.db.habits.update_one(
        {"_id": habit_id},
        {"$set": {"completed": True}}
    )

    return redirect(url_for(".index", date=date_string))


@pages.route("/delete/<habitId>", methods=['POST'])
def delete_habit(habitId):
    current_app.db.habits.delete_one({'_id': habitId})
    return redirect(url_for('.index'))