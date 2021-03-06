#!/usr/bin/env python

import logging

from googleads import dfp

from dfp.client import get_client


logger = logging.getLogger(__name__)


def get_order_by_name(order_name):
  """
  Gets an order by name from DFP.

  Args:
    order_name (str): the name of the DFP order
  Returns:
    a DFP order, or None
  """

  dfp_client = get_client()
  order_service = dfp_client.GetService('OrderService', version='v201702')

  # Filter by name.
  query = 'WHERE name = :name'
  values = [{
    'key': 'name',
    'value': {
      'xsi_type': 'TextValue',
      'value': order_name
    }
  }]
  statement = dfp.FilterStatement(query, values)
  response = order_service.getOrdersByStatement(statement.ToStatement())

  no_order_found = False
  try:
    no_order_found = True if len(response['results']) < 1 else False 
  except (AttributeError, KeyError):
    no_order_found = True

  if no_order_found:
    return None
  else:
    order = response['results'][0]
    logger.info('Found an order with ID "{id}" and name "{name}".'.format(
      id=order['id'], name=order['name']))
    return order

def get_all_orders():
  """
  Logs all orders in DFP.

  Returns:
      None
  """

  dfp_client = get_client()

  # Initialize appropriate service.
  order_service = dfp_client.GetService('OrderService', version='v201702')

  # Create a statement to select orders.
  statement = dfp.FilterStatement()

  # Retrieve a small amount of orders at a time, paging
  # through until all orders have been retrieved.
  while True:
    response = order_service.getOrdersByStatement(statement.ToStatement())
    if 'results' in response:
      for order in response['results']:
        
        print('Found an order with ID "{id}" and name "{name}".'.format(
          id=order['id'], name=order['name']))
      statement.offset += dfp.SUGGESTED_PAGE_LIMIT
    else:
      break

def main():
  get_all_orders()

if __name__ == '__main__':
  main()
