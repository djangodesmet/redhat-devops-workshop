import json
import logging
import os

import requests
from streamlit_tags import st_tags

import streamlit as st

PAGE_TITLE = "Devops course streamlit GUI."


class App:
    def __init__(self, st):
        self.st = st

        # Initialize logger for app errors and catching the exceptions with
        # traceback within the console
        logging.basicConfig(level=logging.INFO)

    @staticmethod
    def get_data():
        input_ids = [[1, 250103, 2986, 250103, 11396, 250103, 8315, 250103,
                   48075, 250104, 260, 94098, 24710, 340, 270, 260,
                   173557, 465, 14925, 260, 261, 19759, 260, 34583,
                   271, 465, 16112, 359, 60675, 264, 290, 465,
                   17514, 349, 465, 9421, 279, 275, 657, 34859,
                   2037, 269, 43680, 18806, 260, 272, 2]]
        attention_mask = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                            1, 1, 1]]
        words_mask = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 3, 4, 5,
                        0, 6, 7, 8, 0, 9, 10, 0, 0, 11, 12, 0, 0, 0, 13, 14,
                        15, 0, 16, 17, 0, 18, 19, 20, 0, 0, 0, 21, 22, 0, 0]]
        text_lengths = [[22]]
        span_idx = [[[0, 0],
                        [0, 1],
                        [0, 2],
                        [0, 3],
                        [0, 4],
                        [0, 5],
                        [0, 6],
                        [0, 7],
                        [0, 8],
                        [0, 9],
                        [0, 10],
                        [0, 11],
                        [1, 1],
                        [1, 2],
                        [1, 3],
                        [1, 4],
                        [1, 5],
                        [1, 6],
                        [1, 7],
                        [1, 8],
                        [1, 9],
                        [1, 10],
                        [1, 11],
                        [1, 12],
                        [2, 2],
                        [2, 3],
                        [2, 4],
                        [2, 5],
                        [2, 6],
                        [2, 7],
                        [2, 8],
                        [2, 9],
                        [2, 10],
                        [2, 11],
                        [2, 12],
                        [2, 13],
                        [3, 3],
                        [3, 4],
                        [3, 5],
                        [3, 6],
                        [3, 7],
                        [3, 8],
                        [3, 9],
                        [3, 10],
                        [3, 11],
                        [3, 12],
                        [3, 13],
                        [3, 14],
                        [4, 4],
                        [4, 5],
                        [4, 6],
                        [4, 7],
                        [4, 8],
                        [4, 9],
                        [4, 10],
                        [4, 11],
                        [4, 12],
                        [4, 13],
                        [4, 14],
                        [4, 15],
                        [5, 5],
                        [5, 6],
                        [5, 7],
                        [5, 8],
                        [5, 9],
                        [5, 10],
                        [5, 11],
                        [5, 12],
                        [5, 13],
                        [5, 14],
                        [5, 15],
                        [5, 16],
                        [6, 6],
                        [6, 7],
                        [6, 8],
                        [6, 9],
                        [6, 10],
                        [6, 11],
                        [6, 12],
                        [6, 13],
                        [6, 14],
                        [6, 15],
                        [6, 16],
                        [6, 17],
                        [7, 7],
                        [7, 8],
                        [7, 9],
                        [7, 10],
                        [7, 11],
                        [7, 12],
                        [7, 13],
                        [7, 14],
                        [7, 15],
                        [7, 16],
                        [7, 17],
                        [7, 18],
                        [8, 8],
                        [8, 9],
                        [8, 10],
                        [8, 11],
                        [8, 12],
                        [8, 13],
                        [8, 14],
                        [8, 15],
                        [8, 16],
                        [8, 17],
                        [8, 18],
                        [8, 19],
                        [9, 9],
                        [9, 10],
                        [9, 11],
                        [9, 12],
                        [9, 13],
                        [9, 14],
                        [9, 15],
                        [9, 16],
                        [9, 17],
                        [9, 18],
                        [9, 19],
                        [9, 20],
                        [10, 10],
                        [10, 11],
                        [10, 12],
                        [10, 13],
                        [10, 14],
                        [10, 15],
                        [10, 16],
                        [10, 17],
                        [10, 18],
                        [10, 19],
                        [10, 20],
                        [10, 21],
                        [11, 11],
                        [11, 12],
                        [11, 13],
                        [11, 14],
                        [11, 15],
                        [11, 16],
                        [11, 17],
                        [11, 18],
                        [11, 19],
                        [11, 20],
                        [11, 21],
                        [11, 22],
                        [12, 12],
                        [12, 13],
                        [12, 14],
                        [12, 15],
                        [12, 16],
                        [12, 17],
                        [12, 18],
                        [12, 19],
                        [12, 20],
                        [12, 21],
                        [12, 22],
                        [12, 23],
                        [13, 13],
                        [13, 14],
                        [13, 15],
                        [13, 16],
                        [13, 17],
                        [13, 18],
                        [13, 19],
                        [13, 20],
                        [13, 21],
                        [13, 22],
                        [13, 23],
                        [13, 24],
                        [14, 14],
                        [14, 15],
                        [14, 16],
                        [14, 17],
                        [14, 18],
                        [14, 19],
                        [14, 20],
                        [14, 21],
                        [14, 22],
                        [14, 23],
                        [14, 24],
                        [14, 25],
                        [15, 15],
                        [15, 16],
                        [15, 17],
                        [15, 18],
                        [15, 19],
                        [15, 20],
                        [15, 21],
                        [15, 22],
                        [15, 23],
                        [15, 24],
                        [15, 25],
                        [15, 26],
                        [16, 16],
                        [16, 17],
                        [16, 18],
                        [16, 19],
                        [16, 20],
                        [16, 21],
                        [16, 22],
                        [16, 23],
                        [16, 24],
                        [16, 25],
                        [16, 26],
                        [16, 27],
                        [17, 17],
                        [17, 18],
                        [17, 19],
                        [17, 20],
                        [17, 21],
                        [17, 22],
                        [17, 23],
                        [17, 24],
                        [17, 25],
                        [17, 26],
                        [17, 27],
                        [17, 28],
                        [18, 18],
                        [18, 19],
                        [18, 20],
                        [18, 21],
                        [18, 22],
                        [18, 23],
                        [18, 24],
                        [18, 25],
                        [18, 26],
                        [18, 27],
                        [18, 28],
                        [18, 29],
                        [19, 19],
                        [19, 20],
                        [19, 21],
                        [19, 22],
                        [19, 23],
                        [19, 24],
                        [19, 25],
                        [19, 26],
                        [19, 27],
                        [19, 28],
                        [19, 29],
                        [19, 30],
                        [20, 20],
                        [20, 21],
                        [20, 22],
                        [20, 23],
                        [20, 24],
                        [20, 25],
                        [20, 26],
                        [20, 27],
                        [20, 28],
                        [20, 29],
                        [20, 30],
                        [20, 31],
                        [21, 21],
                        [21, 22],
                        [21, 23],
                        [21, 24],
                        [21, 25],
                        [21, 26],
                        [21, 27],
                        [21, 28],
                        [21, 29],
                        [21, 30],
                        [21, 31],
                        [21, 32]]]
        span_mask = [[ True,  True,  True,  True,  True,  True,  True,  True,  True,
                True,  True,  True,  True,  True,  True,  True,  True,  True,
                True,  True,  True,  True,  True,  True,  True,  True,  True,
                True,  True,  True,  True,  True,  True,  True,  True,  True,
                True,  True,  True,  True,  True,  True,  True,  True,  True,
                True,  True,  True,  True,  True,  True,  True,  True,  True,
                True,  True,  True,  True,  True,  True,  True,  True,  True,
                True,  True,  True,  True,  True,  True,  True,  True,  True,
                True,  True,  True,  True,  True,  True,  True,  True,  True,
                True,  True,  True,  True,  True,  True,  True,  True,  True,
                True,  True,  True,  True,  True,  True,  True,  True,  True,
                True,  True,  True,  True,  True,  True,  True,  True,  True,
                True,  True,  True,  True,  True,  True,  True,  True,  True,
                True,  True,  True,  True,  True,  True,  True,  True,  True,
                True,  True,  True,  True,  True,  True,  True,  True,  True,
                True,  True,  True,  True,  True,  True,  True,  True, False,
                True,  True,  True,  True,  True,  True,  True,  True,  True,
                True, False, False,  True,  True,  True,  True,  True,  True,
                True,  True,  True, False, False, False,  True,  True,  True,
                True,  True,  True,  True,  True, False, False, False, False,
                True,  True,  True,  True,  True,  True,  True, False, False,
                False, False, False,  True,  True,  True,  True,  True,  True,
                False, False, False, False, False, False,  True,  True,  True,
                True,  True, False, False, False, False, False, False, False,
                True,  True,  True,  True, False, False, False, False, False,
                False, False, False,  True,  True,  True, False, False, False,
                False, False, False, False, False, False,  True,  True, False,
                False, False, False, False, False, False, False, False, False,
                True, False, False, False, False, False, False, False, False,
                False, False, False]]

        data = {
            "inputs": [
                {"name": "attention_mask", "data": attention_mask, "datatype": "INT64", "shape": [1, len(attention_mask[0])]},
                {"name": "input_ids", "data": input_ids, "datatype": "INT64", "shape": [1, len(input_ids[0])]},
                {"name": "span_idx", "data": span_idx, "datatype": "INT64", "shape": [1, len(span_idx[0]), len(span_idx[0][0])]},
                {"name": "span_mask", "data": span_mask, "datatype": "BOOL", "shape": [1, len(span_mask[0])]},
                {"name": "text_lengths", "data": text_lengths, "datatype": "INT64", "shape": [1, 1]},
                {"name": "words_mask", "data": words_mask, "datatype": "INT64", "shape": [1, len(words_mask[0])]},
                ]
                }
        return data


    def gliner_api_handler(self, text, labels, threshold):
        data = {
            "text": text,
            "labels": labels,
            "threshold": threshold,
        }
        endpoint = "predict"
        if not os.getenv("REMOTE"):
            response = requests.post(
                verify=False,
                url=f"http://127.0.0.1:9000/{endpoint}",
                data=json.dumps(data),
            ).json()
        else:
            endpoint = "https://gliner-test-devops-workshop.apps.rosa.rosa-jxx8z.wlcq.p3.openshiftapps.com/v2/models/gliner-test/infer"
            token = os.getenv("SVA_TOKEN")
            headers = {'Authorization': f'Bearer {token}'}
            data = App.get_data()
            response = requests.post(endpoint, json=data, headers=headers).json()
            return response

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
                    st.write(entities)
                    # st.table(entities)

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
