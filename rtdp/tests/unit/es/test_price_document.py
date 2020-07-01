"""Unit tests for the price document"""

import unittest

from rtdp.es.price_document import Tick


class TestPriceDocument(unittest.TestCase):
    """Tests class for price document."""
    price_data = {'time': {
        'updated': 'Jul 1, 2020 18:21:00 UTC',
        'updatedISO': '2020-07-01T18:21:00+00:00',
        'updateduk': 'Jul 1, 2020 at 19:21 BST'},
                  'disclaimer': 'This data was produced from the CoinDesk Bitcoin Price Index (USD). Non-USD currency data converted using hourly conversion rate from openexchangerates.org', #pylint: disable=line-too-long
                  'bpi': {
                      'USD': {
                          'code': 'USD',
                          'rate': '9,284.7576',
                          'description': 'United States Dollar',
                          'rate_float': 9284.7576},
                      'XBT': {
                          'code': 'XBT',
                          'rate': '1.0000',
                          'description': 'Bitcoin',
                          'rate_float': 1}}}

    def test_price_document(self) -> None:
        """Test the price document creation and fields"""
        price_doc = Tick(self.price_data)
        self.assertEqual(type(price_doc.meta.id), str)
        self.assertEqual(price_doc.price, self.price_data['bpi']['USD']['rate_float'])
        self.assertEqual(price_doc.ticker, self.price_data['bpi']['XBT']['code'])
        self.assertEqual(price_doc.currency, self.price_data['bpi']['USD']['code'])
        self.assertEqual(price_doc.event_time, self.price_data['time']['updatedISO'])
