"""
SmartHire AI - Timer & Tab Monitoring Component
Mülakat ekranı için canlı 90 saniyelik geri sayım sayacı ve sekme değiştirme (Tab Switch / Window Blur) güvenlik kontrolü.
"""

import streamlit as st

def render_interview_timer(seconds_left: int = 90, session_id: str = "default"):
    """
    Canlı her saniye güncellenen geri sayım sayacı ve Sekme / Pencere kontrolü (Tab switch detection).
    """
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: 'Inter', system-ui, -apple-system, sans-serif;
                margin: 0;
                padding: 0;
                background: transparent;
            }}
            .timer-card {{
                background: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
                padding: 14px 18px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            }}
            .timer-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 8px;
            }}
            .timer-title {{
                font-size: 13px;
                font-weight: 600;
                color: #475569;
                display: flex;
                align-items: center;
                gap: 6px;
            }}
            .timer-digits {{
                font-size: 18px;
                font-weight: 700;
                font-family: monospace;
                color: #2563EB;
            }}
            .progress-track {{
                width: 100%;
                background: #E2E8F0;
                height: 8px;
                border-radius: 4px;
                overflow: hidden;
            }}
            .progress-fill {{
                height: 100%;
                background: #2563EB;
                width: 100%;
                transition: width 1s linear, background-color 0.5s ease;
            }}
            .tab-warn {{
                display: none;
                margin-top: 8px;
                padding: 8px 12px;
                background: #FEF2F2;
                border: 1px solid #FCA5A5;
                color: #DC2626;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 600;
            }}
        </style>
    </head>
    <body>
        <div class="timer-card">
            <div class="timer-header">
                <div class="timer-title">⏱️ Kalan Mülakat Süresi</div>
                <div class="timer-digits" id="timer-text">01:30</div>
            </div>
            <div class="progress-track">
                <div class="progress-fill" id="progress-bar"></div>
            </div>
            <div class="tab-warn" id="tab-warn">⚠️ Dikkat: Sekme değiştirdiniz! Mülakat odağını koruyun.</div>
        </div>

        <script>
            let totalSeconds = {seconds_left};
            let currentSeconds = totalSeconds;
            let timerElement = document.getElementById('timer-text');
            let progressBar = document.getElementById('progress-bar');
            let tabWarn = document.getElementById('tab-warn');
            let tabAwayTime = 0;
            let tabCheckInterval = null;

            function updateDisplay() {{
                let mins = Math.floor(currentSeconds / 60);
                let secs = currentSeconds % 60;
                timerElement.innerText = (mins < 10 ? '0' : '') + mins + ':' + (secs < 10 ? '0' : '') + secs;

                let pct = (currentSeconds / totalSeconds) * 100;
                progressBar.style.width = pct + '%';

                if (pct < 20) {{
                    progressBar.style.backgroundColor = '#EF4444';
                    timerElement.style.color = '#EF4444';
                }} else if (pct < 50) {{
                    progressBar.style.backgroundColor = '#F59E0B';
                    timerElement.style.color = '#F59E0B';
                }}
            }}

            let countdown = setInterval(function() {{
                if (currentSeconds > 0) {{
                    currentSeconds--;
                    updateDisplay();
                }} else {{
                    clearInterval(countdown);
                }}
            }}, 1000);

            // Sekme Değiştirme (Visibility & Blur Control)
            document.addEventListener('visibilitychange', function() {{
                if (document.hidden) {{
                    tabWarn.style.display = 'block';
                }} else {{
                    tabWarn.style.display = 'none';
                }}
            }});
        </script>
    </body>
    </html>
    """
    st.iframe(html_code, height=95)
