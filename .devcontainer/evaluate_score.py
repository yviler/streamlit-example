from modeling import scoring 

def evaluate_score(conn, txt_jawaban_student, course_info, task_info, soal):
  student_score = 0  # Implement your scoring logic here
  bahasa = 0
  
  if course_info == 'Bahasa Inggris':
    bahasa = 1
  student_score = scoring(conn, txt_jawaban_student, course_info, task_info, soal, bahasa)
  #st.write("\nPredicted Score:", student_score)
  #with st.sidebar:
      #st.text_input('Nilai', value=student_score, max_chars=10, disabled=True, label_visibility="visible")
  return student_score
