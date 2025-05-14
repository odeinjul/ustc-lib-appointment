# USTC LIB APPOINTMENT
[![Lib Appointment](https://github.com/odeinjul/ustc-lib-appointment/actions/workflows/appointment.yml/badge.svg)](https://github.com/odeinjul/ustc-lib-appointment/actions/workflows/appointment.yml)

## Workaround
As passport.ustc.edu.cn/ is deprecated and replaced by id.ustc.edu.cn, 
the original code is not working anymore. A temporary workaround is:

1. Login to hs.lib.ustc.edu.cn,
2. Open the developer tools (F12),
3. Make an appointment,
4. Find and copy the request by right-clicking on it and selecting "Copy as cURL",
5. Replace the date and time in the cURL command with the desired date and time,
6. Run the modified cURL command in the terminal.


