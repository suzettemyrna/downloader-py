# Displaying info

def print_in_process_message(task_objs):
    print("\033[H\033[J", end="")
    print(f"Waiting for the download of {len(task_objs)} files to finish:")

    headers = ["Link", "Status"]

    rows = [(t.link, t.status) for t in task_objs]

    print_table(headers, rows)


def print_final_table(tasks):
    print("\033[H\033[J", end="")
    
    headers = ["Link", "Status"]

    rows = [(t.link, t.status) for t in tasks]

    print_table(headers, rows)


def print_table(headers, rows):
    col_widths = [len(h) for h in headers]

    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))


    def print_separator():
        print("+" + "+".join("-" * (w + 2) for w in col_widths) + "+")

    
    def print_row(row):
        print(
            "|"
            + "|".join(f" {str(cell).ljust(col_widths[i])} " for i, cell in enumerate(row))
            + "|"
        )


    print_separator()
    print_row(headers)
    print_separator()

    for row in rows:
        print_row(row)

    print_separator()