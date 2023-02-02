import justpy as jp
from kgl_event_prediction.simpleEventPredictor import SimpleEventPredictor


input_classes = "m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"
p_classes = 'text-gray-500 m-2 p-2 h-32 text-xl border-2'


class WebPagePredictor(jp.Div):

    def __init__(self, **kwargs):
        super(WebPagePredictor, self).__init__(**kwargs)

        self.input_series = jp.Input(a=self, classes=input_classes, placeholder='Event Series ID')
        self.btn_predict = jp.Button(a=self, classes='bg-green-500 hover:bg-green-700 text-white font-bold '
                                                     'py-2 px-4 rounded-full', text='Predict next event',
                                     on_click=self.on_click_predict)
        self.div_results = jp.Div(a=self, text='Next event loading...', classes=p_classes)

    def on_click_predict(self, msg):
        seriesId = self.input_series.value
        self.div_results.text = 'Next event: ' + seriesId

        # creates an Event Predictor object that can be used to predict a single event or passed to seriesAnalysis to evaluate
        simple_ev = SimpleEventPredictor()

        # sets up the eventPredictor with a series
        simple_ev.initialize(seriesId)

        # predicts the next event
        event = simple_ev.get_next_event()
        self.div_results.text += ' ' + str(event.title) + ' takes place in the year ' + str(event.year)


def predictor_app(request):
    wp = jp.WebPage()
    WebPagePredictor(a=wp)
    return wp


jp.justpy(predictor_app)
