import flet
from flet import *
from datetime import datetime
import sqlite3

# lets create the form class first so we can get some data

class Database:
    try:
        def ConnectToDatabase():
            db = sqlite3.connect('todo.db')
            c = db.cursor()
            c.execute(
                'CREATE TABLE IF not exists tasks (id INTEGER PRIMARY KEY, Task VARCHAR(255) NOT NULL, Date VARCHAR(255) NOT NULL)'
                  )
            return  db
    except Exception as e:
        print(e)

    def ReadDatabase(db):
        c = db.cursor()
        # make sure name the columns and not Slect * From
        c.execute("SELECT Task, Date FROM tasks")
        records = c.fetchall()
        return records

    def InsertDatabase(db, values):
        # also make sute the use ¹ for the inputs for security purposes
        c = db.cursor()
        c.execute("INSERT INTO tasks (Task, Date) VALUES (?,?)", values)
        db.commit()

    def DeleteDatabe(db, values):
        c = db.cursor()
        # quick note: were assuming that no two tasks description are the same and as a result we are deleting based on task
        #an ideal app would not do this but instead delete based on the actual immutable database ID. bit dor the sake od the tutorial and lenhght we will do it this way

        c.execute("DELETE FROM tasks WHERE Task=?",values)

    def UpdateDatabase(db, values):
        c = db.cursor()
        c.execute("UPDATE tasks SET Task=? WHERE Task=?", value)
        db.commit()

class FormContainer(UserControl):
    # at this point, we can pass in a function from the main() so we can expand minimize the form
    # go back to the formContainer() and a argument as such
    def __init__(self, func):
        self.func = func
        super().__init__()

    def build(self):
        return Container(
            width=280,
            height=80,
            bgcolor='bluegrey500',
            opacity=0, # mudar depois mudar para 0 e reverter tambem
            border_radius=40,
            margin=margin.only(left=-20, right=-20),
            animate=animation.Animation(400, "decelerate"),
            animate_opacity=200,
            padding=padding.only(top=45, bottom=45),
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    TextField(
                        height=48,
                        width=255,
                        filled=True,
                        text_size=12,
                        color='black',
                        border_color="transparent",
                        hint_text="Descreva ...",
                        hint_style=TextStyle(size=11, color="black"),
                    ),
                    IconButton(
                        content=Text("Add task", color="white"),
                        width=180,
                        height=44,
                        on_click=self.func, # pass function here
                        style=ButtonStyle(
                                bgcolor={'': 'black'},
                                shape={"": RoundedRectangleBorder(radius=8)},
                        )
                    ),
                ]
            )
        )

# now we need a class to generate a task the user adds one
class CreateTask(UserControl):
    def __init__(self, task: str, date:str, func1, func2):
        # create two arguments so ew can pass is the delete function and edit function when we create an instance of this
        self.task = task
        self.date = date
        self.func1 = func1
        self.func2 = func2
        super().__init__()

    def TaskDeleteEdit(self, name, color, func):
        return IconButton(
            icon=name,
            width=30,
            icon_size=18,
            icon_color=color,
            opacity=0,
            animate_opacity=200,
            # to use it we need to keep it in our delete and edut iconbuttons
            on_click= lambda e: func(self.GetContaincerInstance())
        )

# we need a final thing from here, and that is the instance itseld
    # we need the instace identier so taht we can delete ir needs to be delete
    def GetContaincerInstance(self):
        return self # we return the self instance



    def ShowIcons(self,e):
        if e.data == 'true':
            # these are index od each icon
            (
                e.control.content.controls[1].controls[0].opacity,
                e.control.content.controls[1].controls[1].opacity,
            ) = (1, 1)
            e.control.content.update()
        else:
            (
                e.control.content.controls[1].controls[0].opacity,
                e.control.content.controls[1].controls[1].opacity,
            ) = (0, 0)
            e.control.content.update()



    def build(self):
        return Container(
            width=280,
            height=60,
            border=border.all(0.85, "white54"),
            border_radius=8,
            # lets show the icons when we houver over then
            on_hover=lambda e: self.ShowIcons(e), # mudar depois,
            clip_behavior=ClipBehavior.HARD_EDGE,
            padding=10,
            content=Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Column(
                        spacing=1,
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            Text(value=self.task, size=10),
                            Text(value=self.date, size=9, color='white54'),
                        ]
                    ),
                    # icone de delete e sair
                    Row(
                        spacing=0,
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            # make sure to pass the args here firts
                            self.TaskDeleteEdit(icons.DELETE_ROUNDED, "red500", self.func1),
                            self.TaskDeleteEdit(icons.EDIT_ROUNDED, "white70", self.func2),
                        ]
                    )
                ]
            )
        )

def main(page: Page):
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'

    def AddTaskToScreen(e):
        # now , everytime the user adds a task we need to fecth the data nad output ir the main colum
        # there are 2 data we need: the task + the date
        #
        dateTime = datetime.now().strftime("%b %d, %Y %I:%M")


        # db aqui iniciar
        db = Database.ConnectToDatabase() # retornar db
        Database.InsertDatabase(db,(form.content.controls[0].value, dateTime))
        # we habe both values one the date and time and ther other user task
        # fechar a conexao
        db.close()

        # we could also place the db functions within the if startment




        # now recall that we set the form contianer to form variable we can use
        # this now to see if theres aby content in the textfield
        if form.content.controls[0].value:
            _main_column_.controls.append(
                # here we can create an instance of CreanteTask() clas
                CreateTask(
                    # now, it takes two arguments
                    form.content.controls[0].value,
                    dateTime,
                    # now, the instance takes two more arguments when called
                    DeleteFunction,
                    UpdateFunction

                )
            )
            _main_column_.update()

            # we can recall the sow hide function for the form here
            CreateToDoTask(e)
        else:
            db.close() # ter certexa sute ir cleses even if there is no user input
            pass

    def DeleteFunction(e):
        # when we want to delete, recall that these instance are in a list so that means we can simply remove them whwn we want to

        # lets show waht e is
        # so the instance is passed on as e
        _main_column_.controls.remove(e),
        _main_column_.update()
        print(e)

        _main_column_.controls.remove(e)
        _main_column_.update()
        pass

    def UpdateFunction(e):
        # the update needs a little bit more work
        # we want to update from the form, so we need to pass whatecer the user
        #had from the instance back to the form, the change the function
        # and pass it back again
        form.height, form.opacity = 200, 1

        (
            form.content.controls[0].value,
            form.content.controls[1].content.value,
            form.content.controls[1].on_click,
        ) = (
            e.controls[0].content.controls[0].controls[0].value,
            "Atualizada",
        lambda _: FinalizeUpdadte(e))
        form.update()

        # onde the user edits we need to send the correct data back
        def FinalizeUpdadte(e):
            # we can simply reverse the values from absove
            e.controls[0].content.controls[0].controls[0].value = form.content.controls[0].value
            e.controls[0].content.update()
            # so we cand hide hte contieaner
            CreateToDoTask(e)


    # function to show;hide form contianer
    def CreateToDoTask(e):
        # when we click the ADD iconbutton
        if form.height != 200:
            form.height, form.opacity = 200, 1
            form.update()
        else:
            form.height, form.opacity = 80, 0
            # we can remove the values from the textfield too
            form.content.controls[0].value = None
            form.content.controls[1].content.value = "ADD text"
            form.content.controls[1].on_click = lambda e: AddTaskToScreen(e)
            form.update()

    _main_column_ = Column(
        scroll="hidden",
        expand=True,
        alignment=MainAxisAlignment.START,
        controls=[
            Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    # some title stuff...
                    Text(
                        "Lista de afazeres", size=18, weight="bold", color="white"),
                    IconButton(
                        icons.ADD_CIRCLE_ROUNDED,
                        icon_size=18,
                        on_click=lambda e: CreateToDoTask(e),
                    )
                ]
            ),
            Divider(height=8, color="white24"),
        ]
    )

    # set up some bg and main container
    # The generall Ui will copy that of mobile app

    page.add(
        # this is just bg container
        Container(
            width=1500,
            height=800,
            margin=-10,
             bgcolor="bluegray900",
            alignment=alignment.center,
            content=Row(
                alignment=MainAxisAlignment.CENTER,
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    #main container
                    Container(
                        width=280,
                        height=600,
                        bgcolor="#0f0f0f",
                        border_radius=40,
                        border=border.all(0.5, "white"),
                        padding=padding.only(top=35, left=20, right=20),
                        clip_behavior=ClipBehavior.HARD_EDGE, # clip contents to container
                        content=Column(
                            alignment=MainAxisAlignment.CENTER,
                            expand=True,
                            controls=[
                                #main colum here...
                                _main_column_,
                                # Form class here
                                # pass in the argumetn for the form class here
                                FormContainer(lambda e: AddTaskToScreen(e)),

                            ]
                        )
                    )
                ]
            )
        )
    )
    page.update()


    # form container index is ass follows, we can set the long element index as a variable so it  can be called faste and ease
    form = page.controls[0].content.controls[0].content.controls[1].controls[0]
    # now we can call form whener we want to do somenthing with it .

    # now to display it we need to read the database
    #another note flet keeps on refresing whe we call the database function
    #this could be form my code or from flet itself but it should be addresser

    db = Database.ConnectToDatabase()
    # now remeber that the readdatabase() function return the records

    for task in Database.ReadDatabase(db)[::-1]:
        # lets see if the tasks are being saved
        #lets add these to the screen now
        _main_column_.controls.append(
            # same process as before we create an instance of this class
            CreateTask(
                task=[0], # first item of the returnend tuple
                task=[1],
                DeleteFunction,
                UpdateFunction,
            )
        )
    _main_column_.update()

if __name__ == '__main__':
   flet.app(target=main)
#flet.app(target=main)
