import justpy as jp

from kgl_event_prediction.eventPredictor import EventPredictor
from kgl_event_prediction.multiGuessEventPredictor import MultiGuessEventPredictor
from kgl_event_prediction.simpleEventPredictor import SimpleEventPredictor


input_classes = "m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none " \
                "focus:bg-white focus:border-purple-500"
p_classes = 'text-gray-500 m-2 p-2 h-32 text-xl border-2'
check_classes = "m-2 bg-gray-200 border-2 border-gray-200 rounded w-40 py-2 px-4 text-gray-700 focus:outline-none " \
                "focus:bg-white focus:border-purple-500"
check_text_classes = "p-2 text-xl text-gray-500 w-64"
select_classes = 'w-40 text-xl m-4 p-2 bg-white  border rounded'
button_classes = 'bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-full'
link_classes = 'font-medium text-blue-600 underline dark:text-blue-500 hover:no-underline'


class WebPagePredictor(jp.Div):

    def __init__(self, **kwargs):
        super(WebPagePredictor, self).__init__(**kwargs)

        self.event_predictor = "simple"
        self.input_series = jp.Input(a=self, classes=input_classes, placeholder='Event Series ID')

        # creating a dropdown menu to select predictor
        predictors = ['simple', 'multi guess']
        self.select = jp.Select(classes=select_classes, a=self, value='simple', change=self.set_event_predictor)
        for pred in predictors:
            self.select.add(jp.Option(value=pred, text=pred))

        # button to click and predict the event on click
        self.btn_predict = jp.Button(a=self, classes=button_classes, text='Predict next event',
                                     on_click=self.on_click_predict)

        # fields to display events
        self.div_current_event = jp.Div(a=self, text='Last event loading...', classes=p_classes)
        self.div_results = jp.Div(a=self, text='Next event loading...', classes=p_classes)

        # displays the evaluation (success/fail) of the prediction
        self.p_check_text = jp.P(a=self, text="Prediction is correct? ", classes=check_text_classes)
        self.p_check = jp.P(a=self, text="event loading...", classes=check_classes)

    def set_event_predictor(self, msg):

        if self.select.value == "simple":
            self.event_predictor = "simple"
        elif self.select.value == "multi guess":
            self.event_predictor = "multi guess"

    def on_click_predict(self, msg):
        seriesId = self.input_series.value.strip()
        self.div_results.text = 'Next event of: ' + seriesId
        self.div_current_event.text = 'Last event of: ' + seriesId

        event_predictor = None

        if self.event_predictor == "multi guess":
            event_predictor = MultiGuessEventPredictor()
            # sets up the eventPredictor with a series
            event_predictor.initialize(acronym=seriesId)
        else:
            event_predictor = SimpleEventPredictor()
            # sets up the eventPredictor with a series
            event_predictor.initialize(series_id=seriesId)

        # gets last event and its homepage link
        last_event = event_predictor.get_last_event()
        self.div_current_event.text += ' \"' + str(last_event.title) + '\" has taken place in year ' + \
                                       str(last_event.year) + ', homepage: '
        self.div_current_event += jp.A(text=last_event.homepage, href=last_event.homepage, target='blank',
                                       classes=link_classes)

        # predicts the next event and its homepage link
        event = event_predictor.get_next_event()
        self.div_results.text += ' \"' + str(event.title) + '\" takes place in the year ' + str(event.year) + \
                                 ', homepage: '
        self.div_results += jp.A(text=event.homepage, href=event.homepage, target='blank', classes=link_classes)

        self.p_check.text = event_predictor.get_summary()


def predictor_app(request):
    wp = jp.WebPage()
    WebPagePredictor(a=wp)
    return wp


jp.justpy(predictor_app)
