import os
import getpass
import shutil
import sys
sys.path.append('prg_files/prj_mode')
import prj_workon
import noted

username = getpass.getuser()
projects_location = (f"/home/{username}/.noted/projects/")

def create_project():
    new_pro_name = input("Project name: ")
    if ' ' in new_pro_name:
        print("The project name can't contain any spaces!")
        create_project()
    else:
        if os.path.isdir(f"{projects_location}/{new_pro_name}"):
            print("This project already exists!")
            create_project()        
        else:
            os.makedirs(f"{projects_location}/{new_pro_name}")
            print("\033[2J")
            print("\033[0;0H")
            print("Successfully created: {}".format(new_pro_name))
            main()

def print_header():
    print("\033[2J")
    print("\033[0;0H")
    print("-- Noted -- v.1.0 (beta)\n")

def main():
    
    if os.path.isdir(projects_location):
        projects = os.listdir(projects_location)
        if projects:
            print("Your projects: ", ", ".join(projects))
        else:
            print("No projects found!")

        menu_project = input("[1] create project [2] delete project [3] workon project [4] back\n")

        if menu_project in ("[1]", "1", "one"):
            create_project()

        elif menu_project in ("[2]", "2", "two"):
            def delete_note():
                if projects:
                    print("Your projects: ", ", ".join(projects))
                    delete_pro = input("Which project do you want to delete?: ")
                    if os.path.isdir(f"{projects_location}/{delete_pro}"):
                        delte_pro_confermation = input("Are you sure that you want to delete \"{}\"? [y]es [n]o\n".format(delete_pro))
                        if delte_pro_confermation in ("y", "yes", "[y]"):
                            shutil.rmtree(f"{projects_location}/{delete_pro}")
                            print("\033[2J")
                            print("\033[0;0H")
                            print("Successfully deleted!")
                            main()
                        elif delte_pro_confermation in ("n", "no", "[n]"):
                            print("Canceled")
                            main()
    
                    else:
                        print("This note does not exist!")
                        delete_note()
                else:
                    main()
            delete_note()


        elif menu_project in ("[3]", "3", "three"):
            def workon_project():
                projects = os.listdir(projects_location)
                if projects:
                    print("Your projects: ", ", ".join(projects))
                    prj_selection = input("On which project do you want to workon: ")
                    if os.path.isdir(f"{projects_location}/{prj_selection}"):
                        print("\033[2J")
                        print("\033[0;0H")
                        print("Working on: {}".format(prj_selection))
                        prj_workon.main(prj_selection)
                    else:
                        print("\033[2J")
                        print("\033[0;0H")
                        print("There is no project with the name: {}".format(prj_selection))
                        workon_project()

                else:
                    print("No notes found!")
                    main()
            workon_project()
        elif menu_project in ("[4]", "4", "four"):
            print("\033[2J")
            print("\033[0;0H")
            noted.main()
            

    else:
        os.makedirs(projects_location)
        main()