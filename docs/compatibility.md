# Compatibility and limitations

Source targets Android 9 behavior (target 29), min API 26, compile API 34. No INTERNET permission; network-state permissions only display connectivity. The accessibility service requests window-state events without screen content retrieval or key interception. It matches verified Amazon Home identity, uses bounded duplicate suppression and returns to normal Amazon Home through a visible recovery control.

This is accessibility redirection, not a supported system HOME replacement. It cannot guarantee permanence, eliminate all Amazon flashes, survive every firmware update, or become unreplaceable. Standby/reboot results depend on Fire OS service restoration. This public package has not been installed over the personal working launcher. Test it independently before enabling redirection. No boot receiver, polling service, wake lock or repeated restart loop is used.

Settings/HDMI intents are device dependent. If unavailable, use original Fire TV Settings. Do not disable stock Home or OTA. Live video is intentionally omitted from the initial public preview; static gradients avoid decoder load and unlicensed bundled media.
