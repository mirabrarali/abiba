(function () {
    // SASHA SECURITY PROTOCOL

    const eyeArt = `
           .---.
          /     \\
         | () () |
          \\  ^  /
           |||||
           '---'
    [ EYE OF SASHA ]
    `;

    const securityMessage = "%c SASHA SECURITY ENABLED %c System Protected. Monitoring active. \n\n Unauthorized access to Abiba Neuro-Core console is strictly prohibited.";
    const style1 = "background: #00d2ff; color: #000; font-size: 20px; font-weight: bold; padding: 4px 10px; border-radius: 5px;";
    const style2 = "color: #00d2ff; font-size: 14px; font-style: italic;";

    // Create Alert UI
    const alertBox = document.createElement('div');
    alertBox.id = 'sasha-security-alert';
    alertBox.innerHTML = `
        <div style="background: rgba(5, 7, 10, 0.9); backdrop-filter: blur(20px); border: 1px solid rgba(0, 210, 255, 0.3); padding: 20px 40px; border-radius: 100px; color: white; font-family: 'Outfit', sans-serif; display: flex; items-center space-x-4; box-shadow: 0 0 50px rgba(0, 210, 255, 0.2);">
            <div style="width: 20px; height: 20px; background: #00d2ff; border-radius: 50%; margin-right: 15px; animation: pulse 1s infinite;"></div>
            <span style="font-weight: bold; letter-spacing: 0.1em; font-size: 14px; text-transform: uppercase;">Sasha Security: Shortcuts Blocked</span>
        </div>
    `;
    alertBox.style.cssText = "position: fixed; bottom: 40px; left: 50%; transform: translateX(-50%); z-index: 10000; opacity: 0; pointer-events: none;";
    document.body.appendChild(alertBox);

    const styleSheet = document.createElement("style");
    styleSheet.innerText = `
        @keyframes pulse { 0% { opacity: 1; transform: scale(1); } 50% { opacity: 0.5; transform: scale(1.2); } 100% { opacity: 1; transform: scale(1); } }
    `;
    document.head.appendChild(styleSheet);

    function showSecurityAlert() {
        if (typeof gsap !== 'undefined') {
            gsap.to(alertBox, { opacity: 1, y: -20, duration: 0.5, ease: "power4.out" });
            setTimeout(() => {
                gsap.to(alertBox, { opacity: 0, y: 0, duration: 0.5, ease: "power4.in" });
            }, 3000);
        } else {
            alertBox.style.opacity = '1';
            setTimeout(() => { alertBox.style.opacity = '0'; }, 3000);
        }
    }

    function disableInspect() {
        // Clear console repeatedly
        setInterval(() => {
            console.clear();
            console.log("%c" + eyeArt, "color: #00d2ff; font-family: monospace; font-weight: bold;");
            console.log(securityMessage, style1, style2);
        }, 1000);

        // Right click is now ALLOWED per user request

        // Disable shortcuts
        document.addEventListener('keydown', e => {
            if (
                e.keyCode === 123 || // F12
                (e.ctrlKey && e.shiftKey && e.keyCode === 73) || // Ctrl+Shift+I
                (e.ctrlKey && e.shiftKey && e.keyCode === 74) || // Ctrl+Shift+J
                (e.ctrlKey && e.keyCode === 85) // Ctrl+U
            ) {
                e.preventDefault();
                showSecurityAlert();
                return false;
            }
        });
    }

    // Override console to prevent data leakage
    const noop = () => { };
    console.log = noop;
    console.warn = noop;
    console.error = noop;
    console.dir = noop;
    console.table = noop;

    // Start Security
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', disableInspect);
    } else {
        disableInspect();
    }
})();
