﻿  # -*- coding: utf-8 -*-
'''
Test Vincent
---------

'''

import pandas as pd
import vincent
import nose.tools as nt

class TestVincent(object):
    '''Test vincent.py'''
    
    def setup(self):
        '''Setup method'''
        
        self.testvin = vincent.Vega()
                                     
        self.default_vega = {'width': 400, 'height': 200,
                             'viewport': None, 'axes': [],
                             'padding': {'top': 10, 'left': 30, 
                                         'bottom': 20, 'right': 20}, 
                             'data': [{'name': None, 'values': None}], 
                             'marks': [], 'scales': []}
    
    def test_atts(self):
        '''Test init attributes'''
        
        assert self.testvin.width == 400
        assert self.testvin.height == 200
        assert self.testvin.padding == {'top': 10, 'left': 30, 
                                             'bottom': 20, 'right': 20}
        assert self.testvin.viewport == None
        assert self.testvin.vega == self.default_vega
        
    def test_keypop(self):
        '''Test vega build key removal'''
        keys = ['width', 'height', 'padding', 'viewport', 'data', 
                'scales', 'axes', 'marks']
        for key in keys: 
            self.testvin.build_vega(key)
            dict = self.default_vega.copy()
            dict.pop(key)
            assert self.testvin.vega == dict
            
    def test_updatevis(self):
        '''Test updating the visualization'''
        
        self.testvin.update_vis(height=300, width=1000,
                                padding={'bottom': 40,
                                         'left': 40, 
                                         'right': 40,
                                         'top': 40})
        assert self.testvin.width == 1000
        assert self.testvin.height == 300
        assert self.testvin.padding == {'top': 40, 'left': 40, 
                                        'bottom': 40, 'right': 40}
                                             
    def test_build_component(self):
        '''Test component build'''
        
        self.testvin.build_component(scales=[{"domain": {"data": "area",
                                                        "field": "data.z"},
                                              "name":"z", "type":"ordinal", 
                                              "range":"height"}])
        assert self.testvin.scales[-1] == {"domain": {"data": "area",
                                                      "field": "data.z"},
                                           "name":"z", "type":"ordinal", 
                                           "range":"height"}
        assert self.testvin.scales == self.testvin.vega['scales']
        
        self.testvin.build_component(axes=[{"scale": "x", type: "x"},
                                           {"scale": "y", type: "y"},
                                           {"scale": "z", type: "z"}])
                                                                            
        assert self.testvin.axes == [{"scale": "x", type: "x"},
                                     {"scale": "y", type: "y"},
                                     {"scale": "z", type: "z"}]
        assert self.testvin.axes == self.testvin.vega['axes']
        
    def test_update_component(self):
        '''Test component update'''
        
        self.testvin.build_component(axes=[{"scale": "x", type: "x"}])
        self.testvin.update_component('add', 'w', 'axes', 0, 'scale')
        assert self.testvin.axes[0]["scale"] == 'w'
        
        self.testvin.build_component(scales=[{"domain": {"data": "table",
                                                        "field": "data.x"},
                                             "name":"x", "type":"ordinal", 
                                             "range":"width"}], append=False)
        self.testvin.update_component('add', 'data.y', 'scales', 0, 'domain', 
                                      'field')
        assert self.testvin.vega['scales'][0]['domain']['field'] == 'data.y'
        
    def test_tabular_data(self):
        '''Test tabular data input'''
        
        #Lists
        self.testvin.tabular_data([10, 20, 30, 40, 50])
        assert self.testvin.data[0]['values'][0:2] == [{'x': 0, 'y': 10}, 
                                                       {'x': 1, 'y': 20}]
        self.testvin.tabular_data([60, 70, 80, 90, 100], append=True)
        assert self.testvin.data[0]['values'][-2:] == [{'x': 8, 'y': 90}, 
                                                       {'x': 9, 'y': 100}]
        #Dicts                                              
        self.testvin.tabular_data({'A': 10, 'B': 20})
        assert self.testvin.data[0]['values'][0:2] == [{'x': 'A', 'y': 10}, 
                                                       {'x': 'B', 'y': 20}]
        self.testvin.tabular_data({'C': 30, 'D': 40}) 
        assert self.testvin.data[0]['values'][-2:] == [{'x': 'C', 'y': 30}, 
                                                       {'x': 'D', 'y': 40}]
         
        #Dataframes                                                                                                                                                         
        df = pd.DataFrame({'Column 1': [10, 20, 30, 40, 50], 
                           'Column 2': [60, 70, 80, 90, 100]})
        df2 = pd.DataFrame({'Column 1': [60, 70, 80, 90, 100], 
                            'Column 2': [65, 75, 85, 95, 105]})
                            
        self.testvin.tabular_data(df, columns=['Column 1', 'Column 2'])
        assert self.testvin.data[0]['values'][0:2] == [{'x': 10, 'y': 60}, 
                                                       {'x': 20, 'y': 70}]
        self.testvin.tabular_data(df2, columns=['Column 1', 'Column 2'])
        assert self.testvin.data[0]['values'][-2:] == [{'x': 90, 'y': 95}, 
                                                       {'x': 100, 'y': 105}]
    
    def test_axis_title(self): 
        '''Test the addition of axis and title labels'''
        
        self.testvin.axis_label(x_label='Test 1', y_label='Test 2')
        assert self.testvin.data[1]['name'] == 'x_label'
        assert self.testvin.data[1]['values'][0]['label'] == 'Test 1'
        assert self.testvin.data[2]['name'] == 'y_label'
        assert self.testvin.data[2]['values'][0]['label'] == 'Test 2'
        assert self.testvin.padding['bottom'] == 50
        
        self.testvin.axis_label(title='Test 3', y_label='Remove Label')
        assert self.testvin.data[2]['name'] == 'title'
        assert self.testvin.data[2]['values'][0]['label'] == 'Test 3'
        assert len(self.testvin.marks) == 2
        
        self.testvin.axis_label(x_label='Test 1', y_label='Test 2', 
                                horiz_y=True)
        assert len(self.testvin.marks) == 3
        assert len(self.testvin.data) == 4
        assert self.testvin.padding['left'] == 120
        
        self.testvin.axis_label(x_label='Remove Label', y_label='Remove Label', 
                                title = 'Remove Label')
        assert len(self.testvin.data) == 1
        assert not self.testvin.marks
                                                       
    def test_add_subtract(self):
        '''Test add and subtract on some subclasses'''
        
        bar = vincent.Bar()
        area = vincent.Area()
        
        area + ({'value': 'basis'}, 'marks', 0, 'properties', 'enter', 
                'interpolate')
        bar + ('red', 'marks', 0, 'properties', 'hover', 'fill', 'value')
                
        assert area.marks[0]['properties']['enter'].has_key('interpolate')
        assert bar.marks[0]['properties']['hover']['fill']['value'] == 'red'
          
        bar - ('domain', 'scales', 1)
        bar -= ('name', 'scales', 1)
        area - ('scale', 'axes', 0)
        area -= ('type', 'axes', 1)
        
        assert bar.scales[1] == {'nice': True, 'range': 'height'}
        assert area.axes == [{'type': 'x'}, {'scale': 'y'}]
        
    def test_datetimeandserial(self):
        '''Test pandas serialization and datetime parsing'''
        
        import pandas.io.data as web
        all_data = {}
        for ticker in ['AAPL', 'GOOG']:
            all_data[ticker] = web.get_data_yahoo(ticker, '1/1/2004', 
                                                  '1/1/2006')
        price = pd.DataFrame({tic: data['Adj Close']
                              for tic, data in all_data.iteritems()})

        scatter = vincent.Scatter()
        scatter.tabular_data(price, columns=['AAPL', 'GOOG'])   
        assert scatter.data[0]['values'][0]['x'] == 10.49
        nt.assert_is_none(scatter.data[0]['values'][0]['y'])
        
        line = vincent.Line()
        line.tabular_data(price, columns=['AAPL'])
        assert line.data[0]['values'][0]['x'] == 1073030400000
        
        
        
  

        
        
        
        
        
        
        
        
        
        
        
        
        
            

        