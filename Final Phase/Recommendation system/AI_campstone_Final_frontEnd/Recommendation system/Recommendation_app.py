import streamlit as st
import pandas as pd
import joblib
import io

st.set_page_config(page_title="AI Course Recommendation System", layout="centered")

col1, col2 = st.columns([9,1])

with col1:
    st.title("AI Course Recommendation System")

with col2:
    st.image('logo.png', width=350)

MODEL_PATH = 'C:/Users/DELL/Desktop/AI_campstone/Recommendation system/final_rf_model.pkl'
DATASET_PATH = 'C:/Users/DELL/Desktop/AI_campstone/Dataset/courses_final.csv'

model = joblib.load(MODEL_PATH)
courses_df = pd.read_csv(DATASET_PATH)

st.write("### Enter Your Details")

available_majors = courses_df['major'].dropna().unique().tolist()

user_major = st.selectbox("Select your Major", available_majors)
user_gpa = st.number_input("Enter your GPA", min_value=0.0, max_value=4.0, step=0.1)
user_certs = st.number_input("Number of Professional Certifications", min_value=0, step=1)
user_hours = st.number_input("Study Hours Per Week", min_value=0, step=1)
user_delivery = st.selectbox("Preferred Delivery Mode", ['Online', 'Hybrid', 'In-person'])
user_goal = st.text_input("Career Goal (Optional)")
user_difficulty = st.selectbox("Preferred Course Difficulty", ['Easy', 'Moderate', 'Hard'])
user_skills = st.text_input("Interested Skills (Optional)")

if st.button("Get Recommendation"):
    if user_gpa < 2.0:
        st.warning("No Recommendations Available for GPA below 2.0")
    else:
        if user_gpa >= 3.6:
            levels = ['Advanced']
            scale = 'Expert Level'
        elif user_gpa >= 3.0:
            levels = ['Intermediate', 'Advanced']
            scale = 'Intermediate to Expert'
        elif user_gpa >= 2.8:
            levels = ['Beginner', 'Intermediate']
            scale = 'Intermediate Level'
        elif user_gpa >= 2.5:
            levels = ['Beginner', 'Intermediate']
            scale = 'Basic to Intermediate'
        else:
            levels = ['Beginner']
            scale = 'Basic Level'

        major_courses = courses_df[
            (courses_df['major'].str.lower().str.contains(user_major.lower(), na=False)) &
            (courses_df['prerequisite_level'].isin(levels))
        ][['course_name', 'major', 'prerequisite_level', 'average_grade', 'fail_rate', 'delivery_mode']]

        major_courses = major_courses.drop_duplicates(subset='course_name')

        if major_courses.shape[0] < 5:
            extra_courses = courses_df[
                (courses_df['major'].str.lower().str.contains(user_major.lower(), na=False))
            ][['course_name', 'major', 'prerequisite_level', 'average_grade', 'fail_rate', 'delivery_mode']]

            extra_courses = extra_courses.drop_duplicates(subset='course_name')
            major_courses = pd.concat([major_courses, extra_courses]).drop_duplicates(subset='course_name')

        if major_courses.empty:
            fill_courses = courses_df[['course_name', 'major', 'prerequisite_level', 'average_grade', 'fail_rate', 'delivery_mode']].drop_duplicates(subset='course_name').sort_values(by='average_grade', ascending=False).head(5)
            major_courses = fill_courses

        major_courses.rename(columns={'prerequisite_level': 'level'}, inplace=True)

        st.write("### Top Recommended Courses")
        st.dataframe(major_courses)

        st.write("### Skill Level Scale Based on GPA")
        st.success(f"{scale}")

        st.write("### Summary of Your Profile")
        st.markdown(f"**Career Goal:** {user_goal if user_goal else 'Not Provided'}")
        st.markdown(f"**Preferred Delivery Mode:** {user_delivery}")
        st.markdown(f"**Preferred Difficulty:** {user_difficulty}")
        st.markdown(f"**Interested Skills:** {user_skills if user_skills else 'Not Provided'}")

        user_profile = pd.DataFrame({
            'gpa': [user_gpa],
            'certifications': [user_certs],
            'study_hours': [user_hours],
            'career_goal': [user_goal],
            'Preferred_Delivery': [user_delivery],
            'Preferred_Difficulty': [user_difficulty],
            'Interested_Skills': [user_skills],
            'Recommended_Level': [', '.join(levels)],
            'Skill_Scale': [scale]
        })

        user_profile.to_csv('user_recommendation_summary.csv', index=False)
        st.success("Recommendation saved as user_recommendation_summary.csv")