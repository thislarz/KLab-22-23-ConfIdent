import justpy as jp

from kgl_event_prediction.Predictors.multiGuessEventPredictor import MultiGuessEventPredictor
from kgl_event_prediction.Predictors.simpleEventPredictor import SimpleEventPredictor
from kgl_event_prediction.db_util import DbUtil

input_classes = "m-2 bg-gray-200 border-2 border-gray-200 rounded-md w-64 py-2 px-4 text-gray-700 focus:outline-none " \
                "focus:bg-white focus:border-purple-500"
p_classes = 'text-gray-500 m-2 p-2 text-xl border-2'
check_classes = "m-2 border-2 border-gray-200 rounded w-1/2 py-2 px-4 text-gray-700 focus:outline-none " \
                "focus:bg-white focus:border-purple-500"
check_classes_by_state = {
    'good': check_classes + " bg-green-500",
    'okay': check_classes + " bg-yellow-400",
    'bad': check_classes + " bg-red-500",
    'not_found': check_classes + " bg-gray-400",
}
color_classes_by_state = {
    'good': "green-300",
    'okay': "yellow-300",
    'bad': "red-300",
    'not_found': "gray-300",
}
check_text_classes = "p-2 text-xl text-gray-500 w-64"
select_classes = 'w-40 text-xl m-4 p-2 bg-white  border rounded'
button_classes = 'bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-md'
link_classes = 'font-medium text-blue-600 underline dark:text-blue-500 hover:no-underline'

def render_event(parent, type, event, summary, hide_if_empty=True):
    if event is None and hide_if_empty:
        return

    card_div = jp.Div(a=parent, classes="w-full mt-8 border border-gray-200 rounded-lg shadow")
    if event is None:
        card_div.set_class("bg-red-600")
        card_div.set_class("text-center")
    else:
        card_div.set_class("bg-white")

    title_div = jp.Div(a=card_div, text=type, classes="text-center text-gray-500 border-b border-gray-200 rounded-t-lg bg-gray-50")

    if event is None:
        jp.Div(a=card_div, text="No event found", classes="text-white")
        return

    card_content = jp.Div(a=card_div, classes="p-4 text-center")

    jp.H3(a=card_content, text=event.title, classes="mb-2 text-3xl font-bold text-gray-900")

    subtitle_div = jp.Div(a=card_content, text=f"in {event.year}, at ", classes="text-xl")
    jp.A(a=subtitle_div, text=event.homepage, href=event.homepage, target='blank', classes=link_classes)

    if summary is not None:
        #  {check_classes_by_state[summary['verdict']]}
        summary_classes = f"text-center text-gray-900 border-t border-gray-200 rounded-b-lg bg-{color_classes_by_state[summary['verdict']]}"
        summary_div = jp.Div(a=card_div, classes=summary_classes)
        summary_div.text = f"Verdict {summary['verdict'].upper()} | Year {'OK' if summary['year_check'] else 'NOT OK'} | Acronym {'OK' if summary['acronym_check'] else 'NOT OK'} | Title Similarity: {summary['title_similarity']:.2f}"

    return

    div += jp.Div(text=f'Title: \"{event.title}\"')
    div += jp.Div(text=f'Year: {event.year}')
    homepage_div = jp.Div(text="Homepage: ")
    homepage_div += jp.A(text=event.homepage, href=event.homepage, target='blank', classes=link_classes)
    div += homepage_div

    self.p_check.delete()
    self.p_check.text = ""
    self.p_check += jp.Div(text=f"Title Similarity: {summary['title_similarity']:.2f}")
    self.p_check += jp.Div(text=f"Year OK? {'YES' if summary['year_check'] else 'NO'}")
    self.p_check += jp.Div(text=f"Acronym OK? {'YES' if summary['acronym_check'] else 'NO'}")
    self.p_check += jp.Div(text=f"Verdict: {summary['verdict']}")
    self.p_check.classes = check_classes_by_state[summary['verdict']]


class WebPagePredictor(jp.Div):

    def __init__(self, **kwargs):
        super(WebPagePredictor, self).__init__(**kwargs)

        input_div_parent = jp.Div(a=self, classes="text-center")
        input_div = jp.Div(a=input_div_parent, classes="inline-block")

        self.event_predictor = "simple"
        self.input_series = jp.Input(a=input_div, autofocus=True, classes=input_classes, placeholder='Event Acronym')

        # creating a dropdown menu to select predictor
        predictors = ['simple', 'multi guess']
        self.select = jp.Select(classes=select_classes, a=input_div, value='simple', change=self.set_event_predictor)
        for pred in predictors:
            self.select.add(jp.Option(value=pred, text=pred))

        # button to click and predict the event on click
        self.btn_predict = jp.Button(a=input_div, classes=button_classes, text='Predict next events',
                                     on_click=self.on_click_predict)

        self.result_div = jp.Div(a=self)

        # fields to display events
        # self.div_last_known_event = jp.Div(a=self, text='Last event loading...', classes=p_classes)
        # self.div_next_event = jp.Div(a=self, text='Next event loading...', classes=p_classes)
        # self.div_next_next_event = jp.Div(a=self, text='Next next event loading...', classes=p_classes)

        # displays the evaluation (success/fail) of the prediction
        # self.p_check_text = jp.P(a=self, text="Prediction Evaluation: ", classes=check_text_classes)
        # self.p_check = jp.P(a=self, text="event loading...", classes=check_classes_by_state['not_found'])

    def set_event_predictor(self, msg):

        if self.select.value == "simple":
            self.event_predictor = "simple"
        elif self.select.value == "multi guess":
            self.event_predictor = "multi guess"

    def on_click_predict(self, msg):
        seriesId = self.input_series.value.strip().upper()

        self.result_div.delete()

        print(f"predicting next event for {seriesId}")

        last_event = None
        next1_event = None
        next2_event = None
        summary1 = None
        summary2 = None
        db = DbUtil('event_orclone')
        event_series = db.get_series_by_acronym(seriesId)

        if len(event_series) == 0:
            pass
        elif self.event_predictor == "multi guess":
            event_predictor = MultiGuessEventPredictor(event_series)
            next1_event = event_predictor.next_event
            last_event = event_predictor.get_last_event()
            summary1 = event_predictor.get_summery()

            # next2 event not supported
        else:
            event_predictor = SimpleEventPredictor(event_series)
            next1_event = event_predictor.predicted_next_event
            last_event = event_predictor.get_last_event()
            summary1 = event_predictor.get_summery()

            next_next_year = next1_event.year + 1
            event_predictor = SimpleEventPredictor(event_series, earliest_year=next_next_year)
            next2_event = event_predictor.predicted_next_event
            summary2 = event_predictor.get_summery()

        # displays result
        render_event(self.result_div, "Last known event", last_event, None, hide_if_empty=False)
        render_event(self.result_div, "Next+1 event", next1_event, summary1)
        render_event(self.result_div, "Next+2 event", next2_event, summary2)


def predictor_app(request):
    wp = jp.WebPage()
    wp.title = "Event Series Completion: Common Cases First"
    wp.body_classes = "bg-gray-100"
    container = jp.Div(a=wp, classes="max-w-5xl mx-auto py-8 px-4 sm:px-6 lg:px-8")

    # main
    main = jp.Main(a=container, classes="mt-8 bg-white p-8 rounded-lg shadow-lg")
    jp.H1(a=main, text="Event Series Completion: Common Cases First", classes="text-4xl font-bold text-gray-900 mb-8 text-center")
    content = jp.P(a=main, classes="text-lg text-gray-700 leading-relaxed")
    WebPagePredictor(a=content)

    # footer
    footer = jp.Footer(a=container, classes="mt-8 text-center")
    jp.P(a=footer, classes="text-gray-600 text-sm", text="© 2023 Common Cases First. All rights reserved.")
    return wp


jp.justpy(predictor_app)
