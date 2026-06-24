# --- VARIABLES ---
name = "Anand"
age = 25
city = "Hubballi"

# --- DICTIONARY ---
profile = {
    "name": name,
    "age": age,
    "city": city,
    "skills": ["Python", "Git", "VS Code" , "GitHub"]
}

# --- FUNCTION ---
def print_profile(p):
    print("=== User Profile ===")
    print(f"Name  : {p['name']}")
    print(f"Age   : {p['age']}")
    print(f"City  : {p['city']}")
    print("Skills:")
    for skill in p["skills"]:
        print(f"  - {skill}")

# --- IF/ELSE ---
    if len(p["skills"]) >= 3:
        print("Status: Ready to learn AI!")
    else:
        print("Status: Keep adding skills.")

# --- RUN ---
print_profile(profile)