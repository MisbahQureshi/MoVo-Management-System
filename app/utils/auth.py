from functools import wraps
from flask import session, redirect, url_for
import datetime
from ..extensions import mongo

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session and 'employee_id' not in session:
            # Redirect based on session type
            return redirect(url_for('admin.login') if 'admin_id' not in session else url_for('employee.login'))

        # Session timeout handling
        expires_at = session.get('expires_at')
        if expires_at:
            # Convert expires_at to a naive datetime for comparison
            expires_at = datetime.datetime.fromisoformat(expires_at).replace(tzinfo=None)

            # Compare with utcnow (which is a naive datetime)
            if datetime.datetime.utcnow() > expires_at:
                session.clear()
                return redirect(url_for('admin.login') if 'admin_id' in session else url_for('employee.login'))

        return f(*args, **kwargs)
    return decorated_function

def set_session_timeout():
    # Set session timeout to 1 hour from now
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    session['expires_at'] = expires_at.isoformat()
