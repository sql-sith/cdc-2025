#!/usr/bin/python
# AUTHOR : Isaac Palmersheim (TheEngineerGuy404)
# DATE : 2024-11-24
import sqlite3
import datetime
import sys


class FancyText:
    """
    ANSI formatting module for text
    """
    def __init__(self):
        self.seq = ""
    def __str__(self):
        return self.seq + "\x1b[0m"
    def __repr(self):
        return self.__str__()

    def AddText(
        self,
        text: str,
        reset: bool = True
    ) -> object:
        """
        Appends text to sequence
        """
        self.seq += text
        self.seq += "\x1b[0m" if reset else ""
        return self
    def MoveUp(
        self,
        val: int
    ) -> object:
        """
        Moves cursor up n rows
        """
        self.seq += f"\x1b[{val}A"
        return self
    def MoveDown(
        self,
        rows: int
    ) -> object:
        """
        Moves cursor down n rows
        """
        self.seq += f"\x1b[{rows}B"
        return self
    def MoveLeft(
        self,
        columns: int
    ) -> object:
        """
        Moves cursor left n columns
        """
        self.seq += f"\x1b[{columns}C"
        return self
    def MoveRight(
        self,
        columns: int
    ) -> object:
        """
        Moves cursor right n columns
        """
        self.seq += f"\x1b[{columns}D"
        return self
    def MoveTo(
        self,
        x: int,
        y: int
    ) -> object:
        """
        Moves cursor to new position
        """
        self.seq += f"\x1b[{y};{x}H"
        return self
    def SavePosition(
        self
    ) -> object:
        """
        Saves cursor to terminal
        """
        self.seq += "\x1b[s"
        return self
    def LoadPosition(
        self
    ) -> object:
        """
        Loads saved cursor position 
        """
        self.seq += "\x1b[u"
        return self
    def SetForeground(
        self,
        r: int,
        g: int,
        b: int
    ) -> object:
        """
        Sets next text sequences foreground to RGB
        Terminal must support true color
        """
        self.seq += f"\x1b[38;2;{r};{g};{b}m"
        return self
    def SetBackground(
        self,
        r: int,
        g: int,
        b: int
    ) -> object:
        """
        Sets next text sequences background to RGB
        Terminal must support true color
        """
        self.seq += f"\x1b[48;2;{r};{g};{b}m"
        return self
    def MakeBold(
        self
    ) -> object:
        """
        Makes next text sequences bold
        """
        self.seq += "\x1b[1m"
        return self
    def MakeItalic(
        self
    ) -> object:
        """
        Makes next text sequences italic
        """
        self.seq += "\x1b[3m"
        return self
    def MakeUnderlined(
        self
    ) -> object:
        """
        Makes next text sequences underlined
        """
        self.seq += "\x1b[4m"
        return self
class DBWrapper:
    """
    SQLite3/CSV DB Wrapper for C.R.U.D. Event App
    """
    def __init__(
        self,
        driver: str = "csv"
    ) -> None:
        # Use SQLite3 backend
        if driver.lower() == "sqlite3":
            # Connect to DB file
            self._db = sqlite3.connect("./calendar.db", autocommit=True, check_same_thread=True)
            self._curs = self._db.cursor()

            # Construct Table
            self._curs.execute(
                """
                CREATE TABLE IF NOT EXISTS events (
                    name TEXT UNIQUE NOT NULL,
                    start TEXT NOT NULL,
                    end TEXT NOT NULL
                );
                """
            )

            # Set internal flag
            self._sql_enabled = True

        # Use CSV
        else:
            # Validate DB file
            try:
                with open("./calendar.csv", "r") as f:
                    # Check DB header validity
                    if f.readline() != "name,start,end\n":
                        raise FileNotFoundError
            except FileNotFoundError:
                # Construct DB file
                with open("./calendar.csv", "w") as f:
                    f.write("name,start,end\n")
            self._sql_enabled = False
    def Create(
        self,
        name: str,
        start: datetime.datetime,
        end: datetime.datetime
    ) -> None:
        """
        Create an event entry in DB
        """
        # Verify dates
        if (
            end < start
        ): raise ValueError("Start time cannot be after end time!")

        # Use SQLite3
        if self._sql_enabled:
            self._curs.execute(
                """
                INSERT INTO events VALUES(
                    ?,
                    ?,
                    ?
                )
                """,
                (
                    name,
                    start.isoformat(),
                    end.isoformat()
                )
            )
        # Use CSV
        else:
            with open("./calendar.csv", "a") as f:
                f.write(f"{name.lower()},{start.isoformat()},{end.isoformat()}\n")
    def QueryByName(
        self,
        name: str
    ) -> tuple[datetime.datetime, datetime.datetime] | None:
        """
        Query DB by provided name
        """

        # Use SQLite3
        if self._sql_enabled:
            self._curs.execute(
                """
                SELECT
                    start, end
                FROM
                    events
                WHERE
                    name = ?
                """,
                (name,)
            )

            if res := self._curs.fetchone():
                return (
                    datetime.datetime.fromisoformat(res[0]),
                    datetime.datetime.fromisoformat(res[1])
                )
        # Use CSV
        else:
            with open("./calendar.csv", "r") as f:
                for line in f.readlines()[1:]:
                    vals = line.strip("\n").split(",")
                    if vals[0] == name.lower():
                        return (
                            datetime.datetime.fromisoformat(
                                vals[1]
                            ),
                            datetime.datetime.fromisoformat(
                                vals[2]
                            )
                        )
    def QueryByTime(
        self,
        start_time: datetime.datetime,
        end_time: datetime.datetime | None = None
    ) -> list[str] | None:
        """
        Query DB using timestamp or time range.
        """

        # Use SQLite3
        if self._sql_enabled:
            # If range is given
            if end_time:
                start = start_time.isoformat()
                end = end_time.isoformat()
                self._curs.execute(
                    """
                    SELECT
                        name
                    FROM
                        events
                    WHERE
                        ? BETWEEN start AND end
                        OR
                        ? BETWEEN start AND end
                        OR
                        start BETWEEN ? AND ?
                        OR
                        end BETWEEN ? AND ?
                    """,
                    (
                        start,
                        end,
                        start,
                        end,
                        start,
                        end,
                    )
                )
            # If timestamp is given
            else:
                self._curs.execute(
                    """
                    SELECT
                        name
                    FROM
                        events
                    WHERE
                        ? BETWEEN start AND end
                    """,
                    (
                        start_time.isoformat(),
                    )
                )

            # Only return if query is successful
            if query := self._curs.fetchall():
                return [
                    _[0]
                    for _ in query
                ]
            return None
        # Use CSV
        else:
            res = set()
            with open("./calendar.csv", "r") as f:
                for line in f.readlines()[1:]:
                    vals = line.strip("\n").split(",")
                    search_start = datetime.datetime.fromisoformat(vals[1])
                    search_end = datetime.datetime.fromisoformat(vals[2])
                    
                    if end_time:
                        if (
                            (
                                start_time >= search_start
                                and
                                start_time <= search_end
                            )
                            or
                            (
                                end_time >= search_start
                                and
                                end_time <= search_end
                            )
                            or
                            (
                                search_start >= start_time
                                and
                                search_start <= end_time
                            )
                            or
                            (
                                search_end >= start_time
                                and
                                search_end <= end_time
                            )
                        ): res.add(vals[0])
                    else:
                        if (
                            start_time >= search_start
                            and
                            start_time <= search_end
                        ): res.add(vals[0])
                        
            return list(res) if len(res) != 0 else None
    def QueryAll(
        self
    ) -> list[tuple[str, datetime.datetime, datetime.datetime]]:
        """
        Gets all entries in DB
        """

        # Use SQLite3
        if self._sql_enabled:
            # Execute SQLite3 query
            self._curs.execute(
                """
                SELECT *
                FROM events
                """
            )
            if query := self._curs.fetchall():
                return [
                    (
                        _[0],
                        datetime.datetime.fromisoformat(_[1]),
                        datetime.datetime.fromisoformat(_[2])
                    )
                    for _ in query
                ]
        # Use CSV
        else:
            res = []
            with open("./calendar.csv", "r") as f:
                for line in f.readlines()[1:]:
                    vals = line.strip("\n").split(",")
                    res.append(
                        (
                            vals[0],
                            datetime.datetime.fromisoformat(vals[1]),
                            datetime.datetime.fromisoformat(vals[2])
                        )
                    )
            return res
    def UpdateStartTime(
        self,
        name: str,
        new_start: datetime.datetime
    ) -> None:
        """
        Updates start time of given event (if exists)
        """

        # Use SQLite3
        if self._sql_enabled:
            self._curs.execute(
                """
                UPDATE
                    events
                SET
                    start = ?
                WHERE
                    name = ?
                """,
                (
                    new_start.isoformat(),
                    name
                )
            )
        # Use CSV
        else:
            backup = None
            idx = -1
            with open("./calendar.csv", "r") as f:
                backup = list(f.readlines())
                for cnt, line in enumerate(backup):
                    if not cnt: continue
                    vals = line.strip("\n").split(",")
                    if vals[0] == name.lower():
                        idx = cnt
                        break

            tmp = backup[idx].split(",")
            backup[idx] = ",".join(
                [
                    tmp[0],
                    new_start.isoformat(),
                    tmp[2]
                ]
            )
                
            with open("./calendar.csv", "w") as f:
                f.writelines(backup)
    def UpdateEndTime(
        self,
        name: str,
        new_end: datetime.datetime
    ) -> None:
        """
        Updates start time of given event (if exists)
        """

        # Use SQLite3
        if self._sql_enabled:
            self._curs.execute(
                """
                UPDATE
                    events
                SET
                    end = ?
                WHERE
                    name = ?
                """,
                (
                    new_end.isoformat(),
                    name
                )
            )
        # Use CSV
        else:
            backup = None
            idx = -1
            with open("./calendar.csv", "r") as f:
                backup = list(f.readlines())
                for cnt, line in enumerate(backup):
                    if not cnt: continue
                    vals = line.strip("\n").split(",")
                    if vals[0] == name.lower():
                        idx = cnt
                        break

            tmp = backup[idx].split(",")
            backup[idx] = ",".join(
                [
                    tmp[0],
                    tmp[1],
                    new_end.isoformat()
                ]
            )
                
            with open("./calendar.csv", "w") as f:
                f.writelines(backup)
    def Remove(
        self,
        name: str
    ) -> None:
        """
        Deletes entry from DB
        """

        # Use SQLite3
        if self._sql_enabled:
            self._curs.execute(
                """
                DELETE FROM
                    events
                WHERE
                    name = ?
                """,
                (name,)
            )
        # Use CSV
        else:
            backup = []
            with open("./calendar.csv", "r") as f:
                for cnt, line in enumerate(f.readlines()):
                    if cnt == 0:
                        backup.append(line)
                        continue
                    vals = line.strip("\n").split(",")
                    if vals[0] == name.lower():
                        continue
                    backup.append(
                        line
                    )

            with open("./calendar.csv", "w") as f:
                f.writelines(backup)

def create(
    db: DBWrapper
) -> None:
    # Prompt for event parameters
    name = input(
        FancyText()
        .AddText("Enter the name of the event : ")
    ).lower().strip()

    if db.QueryByName(name):
        print(
            FancyText()
            .MakeBold()
            .SetForeground(255, 0, 0)
            .AddText("Event Already Exists!")
        )
        return


    # Catch conversion error
    try:
        start_date = input(
            FancyText()
            .AddText("Enter start time")
            .MakeBold()
            .AddText(" (YYYY-MM-DD HH:MM:SS)")
            .AddText(" : ")
        )
        start_date = datetime.datetime.fromisoformat(start_date)

        end_date = input(
            FancyText()
            .AddText("Enter end time")
            .MakeBold()
            .AddText(" (YYYY-MM-DD HH:MM:SS)")
            .AddText(" : ")
        )
        end_date = datetime.datetime.fromisoformat(end_date)

        # Detect out of order times
        if start_date > end_date:
            # Ask to swap times
            swap = input(
                FancyText()
                .MakeBold()
                .SetForeground(255, 0, 0)
                .AddText("End time cannot be before the start time!\n")
                .AddText("Swap times? [y/N] ")
            ).lower()

            if swap == "y":
                tmp = start_date
                start_date = end_date
                end_date = tmp
            else:
                print("Exiting...")
                return

        db.Create(
            name,
            start_date,
            end_date
        )
    except ValueError as e:
        print(
                FancyText()
                .MakeBold()
                .SetForeground(255, 0, 0)
                .AddText("Invalid Input!\n")
                .SetForeground(255, 0, 0)
                .AddText("You need to input dates and times in ISO 8601 format!")
            )
    else:
        print(
            FancyText()
            .SetForeground(0, 255, 0)
            .AddText("Event successfully created!")
        )
def delete(
    db: DBWrapper
) -> None:
    # Check if event is successfully removed
    name = input(
        FancyText()
        .AddText("Enter the name of the event : ")
    ).lower().strip()

    # Remove if event exists
    if db.QueryByName(name):
        db.Remove(name)
        print(
            FancyText()
            .MakeBold()
            .SetForeground(0, 255, 0)
            .AddText("Event Successfully Removed!")
        )
    else:
        print(
            FancyText()
            .MakeBold()
            .SetForeground(255, 0, 0)
            .AddText("No Such Event!")
        )
def modify(
    db: DBWrapper
) -> None:
    # Get event from user
    name = input(
        FancyText()
        .AddText("Enter name of event to modify : ")
    ).lower().strip()

    # Check if event exists
    if not db.QueryByName(name):
        print(
            FancyText()
            .MakeBold()
            .SetForeground(255, 0, 0)
            .AddText("No Such Event!")
        )
        return

    # Check if to change starting time
    if input(
        FancyText()
        .AddText("Modify starting time? [y/N] ")
    ).lower() == 'y':
        try:
            # Get new timestamp
            time = datetime.datetime.fromisoformat(
                input(
                    FancyText()
                    .AddText("Enter new timestamp")
                    .MakeBold()
                    .AddText(" (YYYY-MM-DD HH:MM:SS)")
                    .AddText(" : ")
                )
            )
            # Verify new timestamp
            if time > db.QueryByName(name)[1]:
                print(
                    FancyText()
                    .MakeBold()
                    .SetForeground(255, 0, 0)
                    .AddText("Start time cannot be after end time!")
                )
                return

            db.UpdateStartTime(
                name,
                time
            )
            print(
                FancyText()
                .MakeBold()
                .SetForeground(0, 255, 0)
                .AddText("Event Successfully Modified!")
            )
        except ValueError:
            print(
                FancyText()
                .MakeBold()
                .SetForeground(255, 0, 0)
                .AddText("Invalid Input!\n")
                .SetForeground(255, 0, 0)
                .AddText("You need to input dates and times in ISO 8601 format!")
            )
            return

    # Check if to change ending time
    if input(
        FancyText()
        .AddText("Modify ending time? [y/N] ")
    ).lower() == 'y':
        try:
            # Get new timestamp
            time = datetime.datetime.fromisoformat(
                input(
                    FancyText()
                    .AddText("Enter new timestamp")
                    .MakeBold()
                    .AddText(" (YYYY-MM-DD HH:MM:SS)")
                    .AddText(" : ")
                )
            )
            # Verify new timestamp
            if db.QueryByName(name)[0] > time:
                print(
                    FancyText()
                    .MakeBold()
                    .SetForeground(255, 0, 0)
                    .AddText("End time cannot be before start time!")
                )
                return

            db.UpdateEndTime(
                name,
                time
            )
            print(
                FancyText()
                .MakeBold()
                .SetForeground(0, 255, 0)
                .AddText("Event Successfully Modified!")
            )
        except ValueError:
            print(
                FancyText()
                .MakeBold()
                .SetForeground(255, 0, 0)
                .AddText("Invalid Input!\n")
                .SetForeground(255, 0, 0)
                .AddText("You need to input dates and times in ISO 8601 format!")
            )
            return
def fetch(
    db: DBWrapper
) -> None:
    # Get name input
    searchwith = input(
        FancyText()
        .MakeBold()
        .AddText("Search by [name/time/ALL] : ")
    ).lower().strip()

    # Fetch all events
    if not searchwith or searchwith == "all":
        # Run SQLite3 query
        events = db.QueryAll()
        
        if events:
            # Iterate through all results
            for event in events:
                print(
                    FancyText()
                    .AddText("\nEvent : ")
                    .MakeBold()
                    .AddText(event[0])
                    .AddText("\n")
                    .AddText("Starting At : ")
                    .MakeBold()
                    .AddText(event[1].date().isoformat(), reset=False)
                    .AddText(" ", reset=False)
                    .AddText(event[1].time().isoformat())
                    .AddText("\nEnding At : ")
                    .MakeBold()
                    .AddText(event[2].date().isoformat(), reset=False)
                    .AddText(" ", reset=False)
                    .AddText(event[2].time().isoformat())
                )
            return
        else:
            print(
                FancyText()
                .MakeBold()
                .SetForeground(255, 0, 0)
                .AddText("No Events Saved!")
            )
            return

    match searchwith:
        case "name":
            # Query for name
            if event := db.QueryByName(
                input(
                    FancyText()
                    .AddText("Enter name to search for : ")
                ).lower()
            ):
                print(
                    FancyText()
                    .MakeBold()
                    .SetForeground(0, 255, 0)
                    .AddText("Event Found!\n")
                    .AddText("Starting at : ")
                    .MakeBold()
                    .AddText(event[0].date().isoformat(), reset=False)
                    .AddText(" ", reset=False)
                    .AddText(event[0].time().isoformat())
                    .AddText("\nEnding at : ")
                    .MakeBold()
                    .AddText(event[1].date().isoformat(), reset=False)
                    .AddText(" ", reset=False)
                    .AddText(event[1].time().isoformat())
                )

            else:
                print(
                    FancyText()
                    .SetForeground(255, 0, 0)
                    .AddText("No such event found!")
                )

        case "time":
            try:
                # Get first time
                a = datetime.datetime.fromisoformat(
                    input(
                        FancyText()
                        .AddText("Enter timestamp to search for")
                        .MakeBold()
                        .AddText(" (YYYY-MM-DD HH:MM:SS)")
                        .AddText(" : ")
                    )
                )
                # Get second time
                b = input(
                    FancyText()
                    .AddText("Enter second timestamp for the range to search in (leave empty to ignore) : ")
                )

                # Search for specific time if second time is empty,
                # Otherwise search with time range
                if res := db.QueryByTime(
                    a,
                    datetime.datetime.fromisoformat(b) if b else None
                ):
                    for event in res:
                        print(
                            FancyText()
                            .MakeBold()
                            .SetForeground(0, 255, 0)
                            .AddText("\nEvent Found!\n")
                            .AddText("Name : ")
                            .AddText(event)
                        )

                else:
                    print(
                        FancyText()
                        .MakeBold()
                        .SetForeground(255, 0, 0)
                        .AddText("No Event Found!")
                    )

            except ValueError as e:
                raise e
                print(
                    FancyText()
                    .MakeBold()
                    .SetForeground(255, 0, 0)
                    .AddText("Invalid Input!\n")
                    .SetForeground(255, 0, 0)
                    .AddText("You need to input dates and times in ISO 8601 format!")
                )
                    
        case _:
            # Catch-all for any other input
            print(
                FancyText()
                .MakeBold()
                .SetForeground(255, 0, 0)
                .AddText("You cannot search by \'", reset=False)
                .AddText(searchwith, reset=False)
                .AddText("\'!")
                .MakeItalic()
                .AddText("\nEnter NAME or TIME instead.")
            )


FUNCTIONS = {
    "help": lambda _: print(
        FancyText()
        .MakeItalic()
        .AddText("A SQLite3-Powered Calendar app in the command-line\n\n")
        .MakeBold()
        .SetForeground(0, 192, 0)
        .AddText("Command-Line Calendar\n")
        .MakeBold()
        .AddText("Usage: ")
        .AddText("python3 calendar.py [ create | delete | modify | fetch ]\n\n")
        .AddText("Available Commands:\n")
        .AddText("\tcreate : Creates an event to be stored\n")
        .AddText("\tdelete : Deletes an event\n")
        .AddText("\tmodify : Modifies an existing event\n")
        .AddText("\tfetch : Gets any and all applicable events via search engine")
    ),
    "create": create,
    "delete": delete,
    "modify": modify,
    "fetch":  fetch,
}

def main():
    db = DBWrapper(
        #driver="sqlite3"
    )

    if len(sys.argv) == 2:
        if func := FUNCTIONS.get(sys.argv[1]):
            func(db)
            return
        else:
            print(
                FancyText()
                .SetForeground(255, 0, 0)
                .AddText(f"No such command \'{sys.argv[1]}\'")
            )
    FUNCTIONS["help"](db)

if __name__ == "__main__": main()