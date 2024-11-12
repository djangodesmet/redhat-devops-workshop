import json
import logging
import os

import requests
from aapy import AAPInvoker
from streamlit_tags import st_tags

import streamlit as st

PAGE_TITLE = "Devops course streamlit GUI."


class App:
    def __init__(self, st):
        self.st = st

        # Initialize logger for app errors and catching the exceptions with
        # traceback within the console
        logging.basicConfig(level=logging.INFO)

    def gliner_api_handler(self, text, labels, threshold):
        data = {
            "text": text,
            "labels": labels,
            "threshold": threshold,
        }
        endpoint = "predict"
        if not os.getenv("NAMESPACE"):
            response = requests.post(
                verify=False,
                url=f"http://127.0.0.1:9000/{endpoint}",
                data=json.dumps(data),
            ).json()
        else:
            invoker = AAPInvoker(
                name_of_api=os.getenv("API_APP_NAME"),
                namespace=os.getenv("NAMESPACE"),
                platform=os.getenv("PLATFORM"),
            )
            response = invoker.post_request(data, endpoint)["content"]

        return response["entities"]

    def main(self):
        logging.basicConfig(level=logging.INFO)
        # HOME PAGE OF STREAMLIT APP

        self.st.set_page_config(page_title=PAGE_TITLE)

        st.title("🔎 Multilingual NER with Gliner")

        with st.form("gliner"):
            st.write(
                "GLiNER is een multilingual Named Entity Recognition (NER)"
                " model dat elk entiteitstype kan herkennen door labels te definieren"
                " voor de gewenste typen"
                " ([meer info](https://github.com/urchade/GLiNER/))."
            )
            text = st.text_area(
                "Tekst voor NER",
                "Willem Alexander is de koning van Nederland."
                " Hij houdt van sinaasappels en van Armin van Buren"
                " (een wereldberoemde DJ).",
            )

            # Labels for entity prediction
            labels = st_tags(
                label="NER labels:",
                text="Druk enter om toe te voegen",
                value=["person", "country", "food", "dj"],
            )

            threshold = st.slider(
                "Threshold score (hoger is selectiever)", 0.0, 1.0, 0.5, 0.1
            )
            submitted = st.form_submit_button("Submit")
            if submitted:
                with st.spinner("Wait for it..."):
                    # Perform entity prediction

                    entities = self.gliner_api_handler(text, labels, threshold)

                    # Display predicted entities and their labels
                    st.divider()
                    st.write("Gevonden entiteiten:")
                    st.table(entities)

    def run(self):
        """Method to run the app while catching errors and showing them in the UI"""
        try:
            self.main()
        except Exception as e:
            error_message = f"Er ging iets mis! {e}"
            self.st.error(error_message)
            logging.exception(error_message)


if __name__ == "__main__":
    app = App(st)
    app.run()
