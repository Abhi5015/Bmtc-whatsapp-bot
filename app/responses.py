class response_builder:

    @staticmethod
    def greeting():
        return {
            "reply": (
                "👋 Hello! I'm your BMTC assistant.\n\n"
                "Ask me about:\n"
                "• Next bus\n"
                "• Routes\n"
                "• Fares\n\n"
                "Type *help* to see examples."
            )
        }

    @staticmethod
    def help():
        return {
            "reply": (
                "🚌 *BMTC Bot Help*\n\n"
                "Try:\n"
                "• Next bus from Majestic to Hebbal\n"
                "• Route 500D\n"
                "• Fare from BTM to Silk Board"
            )
        }

    @staticmethod
    def next_bus(from_stop, to_stop, stop_name=None):
        if from_stop and to_stop:
            return {
                "reply": (
                    f"🚌 Next buses from *{from_stop}* to *{to_stop}*:\n"
                    "• 500D – arriving in 6 mins\n"
                    "• G-4 – arriving in 12 mins\n\n"
                    "_(Demo data)_"
                )
            }

        if stop_name:
            return {
                "reply": (
                    f"🚌 Next buses at *{stop_name}*:\n"
                    "• 500K – 5 mins\n"
                    "• 335E – 11 mins\n\n"
                    "_(Demo data)_"
                )
            }

        return response_builder.unknown()

    @staticmethod
    def route_info(route):
        return {
            "reply": (
                f"🚌 *Route {route}*\n"
                "Majestic → Hebbal → Yelahanka\n\n"
                "_(Demo route info)_"
            )
        }

    @staticmethod
    def fare(from_stop, to_stop):
        return {
            "reply": (
                f"💰 Fare from *{from_stop}* to *{to_stop}*: ₹25\n\n"
                "_(Estimated)_"
            )
        }

    @staticmethod
    def unknown():
        return {
            "reply": (
                "🤔 I didn't quite understand that.\n\n"
                "Try:\n"
                "• Next bus from Majestic to Hebbal\n"
                "• Route 500D\n"
                "• Fare from BTM to Silk Board"
            )
        }
