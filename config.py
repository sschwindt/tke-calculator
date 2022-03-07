import os as _os


SCRIPT_DIR = _os.path.abspath("") + "/"
NAN = -9999.0

# define data headers
HEADERS = ["File #", "x (m)", "y (m)", "z (m)",
           "u_avr (m/s)", "u_stderr (m/s)", "u_rms (m/s)",
           "v_avr (m/s)", "v_stderr (m/s)", "v_rms (m/s)",
           "w_avr (m/s)", "w_stderr (m/s)", "w_rms (m/s)",
           "k_t (m^2/s^2)", "tau_avr_w (m^2/s^2)", "tau_stderr_w (m^2/s^2)",
           "tau_avr_v (m^2/s^2)", "tau_stderr_v (m^2/s^2)"]
