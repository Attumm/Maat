import os
import sys
import unittest

from deepdiff import DeepDiff as ddiff

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from maat import scale, validate

nested_dict = {
    "data": {
        "people": {
            "34850": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "4855": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "34309": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "5943": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "45435": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "55533": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "23324": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "22223": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "33332": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "3644": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "5675": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "25443": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "4535": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "9654": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "34504": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "90345": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "9645": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "45345": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "7545": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "6342": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "63734": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "453145": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "6453": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "34634": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "1535": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "3453": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "345": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "456": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "45764": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "645": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "744": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "6546": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "2434": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "2352": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "1343": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "1499": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "3384": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "3397": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "3398": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "3399": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "339": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "338": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "337": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "336": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "335": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "334": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "333": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "4": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "5": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "6": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "7": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "8": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "9": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "10": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "11": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "12": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "13": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "14": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "15": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "16": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "17": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "18": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "19": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "20": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "21": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "22": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "23": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "24": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "25": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "26": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "27": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "28": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "29": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "30": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "31": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "32": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "33": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "34": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "35": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "36": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "37": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "38": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "39": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "40": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "41": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "42": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "43": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "44": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "45": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "46": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "47": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "48": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "49": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "50": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "51": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "52": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "53": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "54": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "55": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "56": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "57": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "58": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "59": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "60": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "61": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "62": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "63": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "64": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "65": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "66": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "67": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "68": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "69": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "70": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "71": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "72": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "73": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "74": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "75": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "76": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "77": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "78": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "79": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "80": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "81": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "82": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "8211": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "83": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "84": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "85": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "86": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "87": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "88": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "89": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "90": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "91": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "92": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "93": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "94": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "95": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "96": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "97": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "98": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "99": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },
            "100": {
                "id": 7,
                "name": "John Doe",
                "type": "mimic",
                "x": 823.6228647149701,
                "y": 157.57736006592654,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            },

            "208": {
                "id": 208,
                "name": "John Doe Too",
                "type": "person",
                "x": 434.9446032612515,
                "y": 580.0,
                "address": {
                    'id': 23,
                    'addresses': {
                        'street': {
                            'two': 'deep',
                            '222': 'deep',
                        }
                    }
                }
            }
        },
        "streets": {
            'id': 23,
            'addresses': [
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
                {'street': 'John Doe Street'},
            ]
        }
    }
}
addresses_item = {
    'id': {
        'type': 'int',
        'min_amount': 1
    },
    'addresses': {
        'type': 'dict',
        'nested': {
            'street': {
                'type': 'dict', 'min_amount': 2, 'max_length': 99,
                'nested': {
                    'two': {
                        'type': 'str', 'min_length': 3, 'max_length': 99,
                    },
                    '222': {
                        'type': 'str', 'min_length': 3, 'max_length': 99,
                    },
                }
            }
        }
    }
}

TOPOMAP_ITEM = {
    'id': {
        'type': 'int', 'min_amount': 1
    },
    'name': {
        'type': 'str', 'min_length': 1, 'max_length': 35, 'regex': '([^\s]+)'
    },
    'type': {
        'type': 'str', 'min_length': 1, 'max_length': 25, 'regex': r'([^\s]+)'
    },
    "x": {'type': 'float'},
    "y": {'type': 'float'},
    "address": {
        'type': 'dict',
        'nested': addresses_item
    }
}

nested_dict_validation = {
    'data': {
        'type': 'dict',
        'nested': {
            'people': {
                'type': 'aso_array', 'min_amount': 1, 'max_amount': 23499,
                'nested': TOPOMAP_ITEM
            },
            'streets': {
                'type': 'dict', 
                'nested': {
                    'id': {'type': 'int', 'min_amount': 1
                    },
                    'addresses': {
                        'type': 'list_dicts', 'nested': {
                            'street': {'type': 'str', 'min_length': 5, 'max_length': 99,
                            },
                        }
                    }
                }
            }
        }
    }
}


class TestCornerCasesDict(unittest.TestCase):

    def test_validation(self):
        """Happy path test"""
        validated_items = scale(nested_dict, nested_dict_validation)
        difference = ddiff(validated_items, nested_dict)
        self.assertEqual(difference, {})

        validated_items = validate(nested_dict, nested_dict_validation)
        difference = ddiff(validated_items, nested_dict)

        # if the differ finds no difference a empty dictionary is returned
        self.assertEqual(difference, {})
        

if __name__ == '__main__':
    unittest.main()
