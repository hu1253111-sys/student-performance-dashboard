import pandas as pd
from pathlib import Path

# Load student data
file_path = Path("data/students.csv")
df = pd.read_csv(file_path)

# Calculate total marks
# Total marks for 4 subjects
# Final marks out of 400

df["Total"] = df["Assignment"] + df["Internal"] + df["Practical"] + df["External"]
df["Percentage"] = (df["Total"] / 400) * 100

# Result status
# Pass if percentage >= 40

df["Result"] = df["Percentage"].apply(lambda x: "Pass" if x >= 40 else "Fail")

# Summary statistics
avg_percentage = df["Percentage"].mean()
pass_count = (df["Result"] == "Pass").sum()
fail_count = (df["Result"] == "Fail").sum()

top_students = df.sort_values(by="Percentage", ascending=False).head(5)
branch_avg = df.groupby("Branch")["Percentage"].mean().reset_index()

# Build HTML rows
student_rows = ""
for _, row in df.iterrows():
    student_rows += f"""
    <tr>
        <td>{row['Student_ID']}</td>
        <td>{row['Name']}</td>
        <td>{row['Branch']}</td>
        <td>{row['Semester']}</td>
        <td>{row['Attendance']}</td>
        <td>{row['Percentage']:.2f}%</td>
        <td>{row['Result']}</td>
    </tr>
    """

top_rows = ""
for _, row in top_students.iterrows():
    top_rows += f"""
    <tr>
        <td>{row['Name']}</td>
        <td>{row['Branch']}</td>
        <td>{row['Percentage']:.2f}%</td>
    </tr>
    """

branch_rows = ""
for _, row in branch_avg.iterrows():
    branch_rows += f"""
    <tr>
        <td>{row['Branch']}</td>
        <td>{row['Percentage']:.2f}%</td>
    </tr>
    """

# HTML page
html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Student Performance Dashboard</title>
    <link rel="stylesheet" href="../static/style.css" />
</head>
<body>
    <header>
        <h1>Student Performance Dashboard</h1>
    </header>

    <section class="cards">
        <div class="card">
            <h3>Total Students</h3>
            <p>{len(df)}</p>
        </div>
        <div class="card">
            <h3>Average Percentage</h3>
            <p>{avg_percentage:.2f}%</p>
        </div>
        <div class="card">
            <h3>Pass Students</h3>
            <p>{pass_count}</p>
        </div>
        <div class="card">
            <h3>Fail Students</h3>
            <p>{fail_count}</p>
        </div>
    </section>

    <section class="table-section">
        <h2>Student Performance Records</h2>
        <table>
            <thead>
                <tr>
                    <th>Student ID</th>
                    <th>Name</th>
                    <th>Branch</th>
                    <th>Semester</th>
                    <th>Attendance</th>
                    <th>Percentage</th>
                    <th>Result</th>
                </tr>
            </thead>
            <tbody>
                {student_rows}
            </tbody>
        </table>
    </section>

    <section class="two-columns">
        <div class="panel">
            <h2>Top Students</h2>
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Branch</th>
                        <th>Percentage</th>
                    </tr>
                </thead>
                <tbody>
                    {top_rows}
                </tbody>
            </table>
        </div>

        <div class="panel">
            <h2>Branch-wise Average</h2>
            <table>
                <thead>
                    <tr>
                        <th>Branch</th>
                        <th>Average</th>
                    </tr>
                </thead>
                <tbody>
                    {branch_rows}
                </tbody>
            </table>
        </div>
    </section>
</body>
</html>
"""

# Save output in output folder
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)
(output_dir / "report.html").write_text(html, encoding="utf-8")

print("Dashboard generated successfully. Open output/report.html in your browser.")
