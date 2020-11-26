#python program for goal stack planning
# from time import sleep
init = input('Enter the initial state: ')
goal = input('Enter the goal state: ')

#parsing the predicates
# init = init.replace(" ", "")
init = set(init.split(","))
# goal = goal.replace("", "")
goal = set(goal.split(","))

#defining predicates as set
pdc = {"ontable", "on", "clear", "holding", "armemp"}

#functions for actions
def stack(x, y, db):
    db.remove("holding " + x)
    db.remove("clear " + y)

    db.add("armemp")
    db.add("on " + x + " " + y)
    db.add("clear " + x)

    return

def unstack(x, y, db):
    db.remove("armemp")
    db.remove("on " + x + " " + y)
    db.remove("clear " + x)

    db.add("holding " + x)
    db.add("clear " + y)

    return

def pickup(x, db):
    db.remove("ontable "+ x)
    db.remove("armemp")
    db.remove("clear " + x)

    db.add("holding " + x)

    return

def putdown(x, db):
    db.remove("holding " + x)

    db.add("ontable "+ x)
    db.add("armemp")
    db.add("clear " + x)

    return

#defining data structures
#using list as a stack for goal stack
gstack = []
#using set as a database (current state description, only has predicates)
db = init.copy()    #initializing database with init
#list for solution
sol = []

#algorithm

for x in goal:          #push goals onto stack
    gstack.append(x)

while len(gstack) > 0:
    print("\nGoal Stack: ")
    for x in reversed(gstack):
        print(x)

    word = gstack.pop()   #pop stack
    var = word.split(" ")

    if var[0] in pdc:      #if predicate
        
        y = ' '.join(var)
        print("\nPopped: " + y)

        if y in db:   #if it is in database, then do nothing
            pass

        elif var[0] == "ontable":
            gstack.append("putdown "+ var[1])   #adding relevant action to the goal stack
            gstack.append("holding "+ var[1])   #adding preconditions
            
        elif var[0] == "on":
            gstack.append("stack " + var[1] + " " + var[2])
            gstack.append("holding " + var[1])
            gstack.append("clear " + var[2])

        elif var[0] == "armemp":
            y = ""
            for x in db:
                if "holding" in x:
                    y = x[8]
                    break

            gstack.append("putdown "+ y)
            gstack.append("holding "+ y)

        elif var[0] == "clear":
            if "holding " + var[1] in db:
                gstack.append("putdown "+ var[1])
                gstack.append("holding "+ var[1])
                
            else:
                y = ""
                for x in db:
                    if "on " in x and var[1] in x:
                        y = x[3]
                        break
                
                gstack.append("unstack "+ y + " " + var[1])
                gstack.append("on "+ y + " " + var[1])
                gstack.append("clear "+ y)
                gstack.append("armemp")
    
        elif var[0] == "holding":
            if "ontable " + var[1] in db:
                gstack.append("pickup "+ var[1])
                gstack.append("ontable "+ var[1])
                gstack.append("clear "+ var[1])
                gstack.append("armemp")
              
            else:
                y = ""
                for x in db:
                    if "on " + var[1] in x:
                        y = x[5]
                        break
                
                gstack.append("unstack "+ var[1] + " " + y)
                gstack.append("on "+ var[1] + " " + y)
                gstack.append("clear "+ var[1])
                gstack.append("armemp")

    else:   #if action then update database and solution
        if var[0] == "stack":
            stack(var[1], var[2], db)
            sol.append(var)
        elif var[0] == "unstack":
            unstack(var[1], var[2], db)
            sol.append(var)
        elif var[0] == "pickup":
            if "armemp" not in db:
                gstack.append("pickup " + var[1])
                gstack.append("armemp")
            else:    
                pickup(var[1], db)
                sol.append(var)
        elif var[0] == "putdown":
            putdown(var[1], db)
            sol.append(var)

        print("\nUpdated database:")
        print(db)

#finally doing goal test
if goal.issubset(db):
    print("Goal Plan:")
    for x in sol:
        y = ' '.join(x)
        print(y)

else:
    print("The goal could not be reached")