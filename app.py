from flask import Flask, render_template, request
from utils.data_loader import load_all_data, extract_role_domains, load_login_data
from utils.platform_analysis import best_platform_for_recruiter, best_platform_for_job_seeker

app = Flask(__name__)

# Load all data once
job_datasets = load_all_data()
login_data = load_login_data()
role_domains = extract_role_domains(job_datasets)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/recruiter', methods=['GET', 'POST'])
def recruiter():
    best_platform = None
    if request.method == 'POST':
        role_domain = request.form['role_domain']
        job_mode = request.form['job_mode']
        best_platform = best_platform_for_recruiter(role_domain, job_mode, job_datasets, login_data)
    return render_template('recruiter.html', role_domains=role_domains, best_platform=best_platform)

@app.route('/job_seeker', methods=['GET', 'POST'])
def job_seeker():
    best_platform = None
    if request.method == 'POST':
        role_domain = request.form['role_domain']
        job_mode = request.form['job_mode']
        best_platform = best_platform_for_job_seeker(role_domain, job_mode, job_datasets)
    return render_template('job_seeker.html', role_domains=role_domains, best_platform=best_platform)

if __name__ == '__main__':
    app.run(debug=True)
