import justpy as jp

from kgl_event_prediction.Predictors.multiGuessEventPredictor import MultiGuessEventPredictor
from kgl_event_prediction.Predictors.simpleEventPredictor import SimpleEventPredictor
from kgl_event_prediction.db_util import DbUtil

input_classes = "m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none " \
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
check_text_classes = "p-2 text-xl text-gray-500 w-64"
select_classes = 'w-40 text-xl m-4 p-2 bg-white  border rounded'
button_classes = 'bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-full'
link_classes = 'font-medium text-blue-600 underline dark:text-blue-500 hover:no-underline'

def render_event(div, event):
    if event is None:
        div += jp.Div(text="not supported for this predictor")
        return

    div += jp.Div(text=f'Title: \"{event.title}\"')
    div += jp.Div(text=f'Year: {event.year}')
    homepage_div = jp.Div(text="Homepage: ")
    homepage_div += jp.A(text=event.homepage, href=event.homepage, target='blank', classes=link_classes)
    div += homepage_div


class WebPagePredictor(jp.Div):

    def __init__(self, **kwargs):
        super(WebPagePredictor, self).__init__(**kwargs)

        self.event_predictor = "simple"
        self.input_series = jp.Input(a=self, classes=input_classes, value="iswc", placeholder='Event Acronym')

        # creating a dropdown menu to select predictor
        predictors = ['simple', 'multi guess']
        self.select = jp.Select(classes=select_classes, a=self, value='simple', change=self.set_event_predictor)
        for pred in predictors:
            self.select.add(jp.Option(value=pred, text=pred))

        # button to click and predict the event on click
        self.btn_predict = jp.Button(a=self, classes=button_classes, text='Predict next event',
                                     on_click=self.on_click_predict)

        # fields to display events
        self.div_last_known_event = jp.Div(a=self, text='Last event loading...', classes=p_classes)
        self.div_next_event = jp.Div(a=self, text='Next event loading...', classes=p_classes)
        self.div_next_next_event = jp.Div(a=self, text='Next next event loading...', classes=p_classes)

        # displays the evaluation (success/fail) of the prediction
        self.p_check_text = jp.P(a=self, text="Prediction Evaluation: ", classes=check_text_classes)
        self.p_check = jp.P(a=self, text="event loading...", classes=check_classes_by_state['not_found'])

    def set_event_predictor(self, msg):

        if self.select.value == "simple":
            self.event_predictor = "simple"
        elif self.select.value == "multi guess":
            self.event_predictor = "multi guess"

    def on_click_predict(self, msg):
        seriesId = self.input_series.value.strip().upper()

        self.div_last_known_event.delete()
        self.div_next_event.delete()
        self.div_next_next_event.delete()

        self.div_last_known_event.text = 'Most recent known event of ' + seriesId
        self.div_next_event.text = 'Predicted next event of ' + seriesId
        self.div_next_next_event.text = 'Predicted next next event of ' + seriesId

        print(f"predicting next event for {seriesId}")

        event_predictor = None
        db = DbUtil('event_orclone')
        event_series = db.get_series_by_acronym(seriesId)

        if len(event_series) == 0:
            s = f"Series '{seriesId}' does not exist"
            self.div_next_event.text = s
            self.div_last_known_event.text = s
            return

        if self.event_predictor == "multi guess":
            event_predictor = MultiGuessEventPredictor(event_series)
            next_event = event_predictor.next_event
            next_next_event = None  # not supported
            last_event = event_predictor.get_last_event()
        else:
            event_predictor = SimpleEventPredictor(event_series)
            next_event = event_predictor.predicted_next_event
            last_event = event_predictor.get_last_event()

            next_next_year = next_event.year + 1
            event_predictor = SimpleEventPredictor(event_series, earliest_year=next_next_year)
            next_next_event = event_predictor.predicted_next_event

        # displays result
        render_event(self.div_last_known_event, last_event)
        render_event(self.div_next_event, next_event)
        render_event(self.div_next_next_event, next_next_event)

        summary = event_predictor.get_summery()
        self.p_check.delete()
        self.p_check.text = ""
        self.p_check += jp.Div(text=f"Title Similarity: {summary['title_similarity']:.2f}")
        self.p_check += jp.Div(text=f"Year OK? {'YES' if summary['year_check'] else 'NO'}")
        self.p_check += jp.Div(text=f"Acronym OK? {'YES' if summary['acronym_check'] else 'NO'}")
        self.p_check += jp.Div(text=f"Verdict: {summary['verdict']}")
        self.p_check.classes = check_classes_by_state[summary['verdict']]


def predictor_app(request):
    wp = jp.WebPage()
    WebPagePredictor(a=wp)
    return wp


jp.justpy(predictor_app)
