# Rent table and the card list

# Color, rents for # of properties, property needed for a set
rent_table = [
    ['Red', [[1, 2], [2, 3], [3, 6]]],
    ['Yellow', [[1, 2], [2, 4], [3, 6]]],
    ['Light Blue', [[1, 1], [2, 2], [3, 3]]],
    ['Black', [[1, 2], [2, 2], [3, 3], [3, 4]]],
    ['Brown', [[1, 1], [2, 2]]],
    ['Green', [[1, 2], [2, 4], [3, 7]]],
    ['Purple', [[1, 1], [2, 2], [3, 4]]],
    ['Orange', [[1, 1], [2, 3], [3, 5]]],
    ['Dark Blue', [[1, 3], [2, 8]]],
    ['Electric', [[1, 1], [2, 2]]],
    ['Water', [[1, 1], [2, 2]]]
]

card_list = [
    ['Wild Property', 'Property', ['Red', 'Yellow', 'Light Blue', 'Black', 'Brown', 'Green', 'Purple', 'Orange',
                                   'Dark Blue', 'Electric', 'Water'], 'None', 0, 2],
    ['Water Works', 'Property', ['Water'], 'Water', 2, 1],
    ['Electric Company', 'Property', ['Electric'], 'Electric', 2, 1],
    ['Red & Yellow Wild', 'Property', ['Red', 'Yellow'], 'None', 3, 2],
    ['Indiana Avenue', 'Property', ['Red'], 'Red', 3, 1],
    ['Illinois Avenue', 'Property', ['Red'], 'Red', 3, 1],
    ['Kentucky Avenue', 'Property', ['Red'], 'Red', 3, 1],
    ['Marvin Gardens', 'Property', ['Yellow'], 'Yellow', 3, 1],
    ['Marvin Gardens', 'Property', ['Yellow'], 'Yellow', 3, 1],
    ['Atlantic Avenue', 'Property', ['Yellow'], 'Yellow', 3, 1],
    ['Oriental Avenue', 'Property', ['Light Blue'], 'Light Blue', 1, 1],
    ['Vermont Avenue', 'Property', ['Light Blue'], 'Light Blue', 1, 1],
    ['Connecticut Avenue', 'Property', ['Light Blue'], 'Light Blue', 1, 1],
    ['Light Blue & Black Wild', 'Property', ['Light Blue', 'Black'], 'None', 4, 1],
    ['Light Blue & Brown Wild', 'Property', ['Light Blue', 'Brown'], 'None', 1, 1],
    ['Mediterranean Avenue', 'Property', ['Brown'], 'Brown', 1, 1],
    ['Baltic Avenue', 'Property', ['Brown'], 'Brown', 1, 1],
    ['Pennsylvania Railroad', 'Property', ['Black'], 'Black', 2, 1],
    ['Short Line', 'Property', ['Black'], 'Black', 2, 1],
    ['Reading Railroad', 'Property', ['Black'], 'Black', 2, 1],
    ['B&O Railroad', 'Property', ['Black'], 'Black', 2, 1],
    ['Black & Electric Wild', 'Property', ['Black', 'Electric'], 'None', 2, 1],
    ['Black & Green Wild', 'Property', ['Black', 'Green'], 'None', 4, 1],
    ['Pennsylvania Avenue', 'Property', ['Green'], 'Green', 4, 1],
    ['Pacific Avenue', 'Property', ['Green'], 'Green', 4, 1],
    ['North Caroline Avenue', 'Property', ['Green'], 'Green', 4, 1],
    ['Green & Dark Blue Wild', 'Property', ['Green', 'Dark Blue'], 'None', 4, 1],
    ['St. Charles Place', 'Property', ['Purple'], 'Purple', 2, 1],
    ['Virginia Avenue', 'Property', ['Purple'], 'Purple', 2, 1],
    ['States Avenue', 'Property', ['Purple'], 'Purple', 2, 1],
    ['Purple & Orange Wild', 'Property', ['Purple', 'Orange'], 'None', 2, 2],
    ['Tennessee Avenue', 'Property', ['Orange'], 'Orange', 2, 1],
    ['New York Avenue', 'Property', ['Orange'], 'Orange', 2, 1],
    ['St. James Place', 'Property', ['Orange'], 'Orange', 2, 1],
    ['Boardwalk', 'Property', ['Dark Blue'], 'Dark Blue', 4, 1],
    ['Park Place', 'Property', ['Dark Blue'], 'Dark Blue', 4, 1],

    ['Rent - Wild', 'Rent', ['Red', 'Yellow', 'Light Blue', 'Black', 'Brown', 'Green', 'Purple', 'Orange',
                             'Dark Blue', 'Electric', 'Water'], 'None', 3, 3],
    ['Rent - Red & Yellow', 'Rent', ['Red', 'Yellow'], 'None', 1, 2],
    ['Rent - Dark Blue & Green', 'Rent', ['Dark Blue', 'Green'], 'None', 1, 2],
    ['Rent - Orange & Purple', 'Rent', ['Orange', 'Purple'], 'None', 1, 2],
    ['Rent - Light Blue & Brown', 'Rent', ['Light Blue', 'Brown'], 'None', 1, 2],
    ['Rent - Black & Electric', 'Rent', ['Black', 'Electric'], 'None', 1, 1],
    ['Rent - Black & Water', 'Rent', ['Black', 'Water'], 'None', 1, 1],

    ['Pass Go', 'Action', ['None'], 'None', 1, 10],
    ['Birthday!', 'Action', ['None'], 'None', 2, 3],
    ['Debt Collector', 'Action', ['None'], 'None', 3, 3],
    ['Sly Deal', 'Action', ['None'], 'None', 3, 3],
    ['Forced Deal', 'Action', ['None'], 'None', 3, 3],
    ['Just Say No', 'Action', ['None'], 'None', 4, 3],
    ['Deal Breaker', 'Action', ['None'], 'None', 5, 2],
    ['Double the Rent', 'Action', ['None'], 'None', 1, 2],

    ['$1', 'Money', ['None'], 'None', 1, 6],
    ['$2', 'Money', ['None'], 'None', 2, 5],
    ['$3', 'Money', ['None'], 'None', 3, 3],
    ['$4', 'Money', ['None'], 'None', 4, 3],
    ['$5', 'Money', ['None'], 'None', 5, 2],
    ['$10', 'Money', ['None'], 'None', 10, 1],

    ['House', 'House', ['None'], 'None', 3, 3],
    ['Hotel', 'Hotel', ['None'], 'None', 4, 2]

]

test_card_list = [
    ['Just Say No', 'Action', ['None'], 'None', 4, 1],
    ['Wild Property', 'Property', ['Red', 'Yellow', 'Light Blue', 'Black', 'Brown', 'Green', 'Purple', 'Orange',
                                   'Dark Blue', 'Electric', 'Water'], 'None', 0, 2],

    ['Rent - Wild', 'Rent', ['Red', 'Yellow', 'Light Blue', 'Black', 'Brown', 'Green', 'Purple', 'Orange',
                             'Dark Blue', 'Electric', 'Water'], 'None', 3, 3],
    ['Red & Yellow Wild', 'Property', ['Red', 'Yellow'], 'None', 3, 2],
    ['Rent - Red & Yellow', 'Rent', ['Red', 'Yellow'], 'None', 1, 2],

    ['Indiana Avenue', 'Property', ['Red'], 'Red', 3, 1],
    ['Just Say No', 'Action', ['None'], 'None', 4, 1],
    ['Sly Deal', 'Action', ['None'], 'None', 3, 3],
    ['Forced Deal', 'Action', ['None'], 'None', 3, 3],
    ['Birthday!', 'Action', ['None'], 'None', 2, 3],
    ['Debt Collector', 'Action', ['None'], 'None', 3, 3],

    ['Illinois Avenue', 'Property', ['Red'], 'Red', 3, 1],
    ['Kentucky Avenue', 'Property', ['Red'], 'Red', 3, 1],

    ['Marvin Gardens', 'Property', ['Yellow'], 'Yellow', 3, 1],
    ['Marvin Gardens', 'Property', ['Yellow'], 'Yellow', 3, 1],
    ['Atlantic Avenue', 'Property', ['Yellow'], 'Yellow', 3, 1],
    ['Oriental Avenue', 'Property', ['Light Blue'], 'Light Blue', 1, 1],
    ['Vermont Avenue', 'Property', ['Light Blue'], 'Light Blue', 1, 1],
    ['Just Say No', 'Action', ['None'], 'None', 4, 3],
    ['Connecticut Avenue', 'Property', ['Light Blue'], 'Light Blue', 1, 1],
    ['Light Blue & Black Wild', 'Property', ['Light Blue', 'Black'], 'None', 4, 1],
    ['Light Blue & Brown Wild', 'Property', ['Light Blue', 'Brown'], 'None', 1, 1],
    ['Mediterranean Avenue', 'Property', ['Brown'], 'Brown', 1, 1],
    ['Baltic Avenue', 'Property', ['Brown'], 'Brown', 1, 1],
    ['Pennsylvania Railroad', 'Property', ['Black'], 'Black', 2, 1],
    ['Short Line', 'Property', ['Black'], 'Black', 2, 1],
    ['Reading Railroad', 'Property', ['Black'], 'Black', 2, 1],
    ['B&O Railroad', 'Property', ['Black'], 'Black', 2, 1],
    ['Black & Electric Wild', 'Property', ['Black', 'Electric'], 'None', 2, 1],
    ['Black & Green Wild', 'Property', ['Black', 'Green'], 'None', 4, 1],
    ['Pennsylvania Avenue', 'Property', ['Green'], 'Green', 4, 1],
    ['Pacific Avenue', 'Property', ['Green'], 'Green', 4, 1],
    ['North Caroline Avenue', 'Property', ['Green'], 'Green', 4, 1],
    ['Green & Dark Blue Wild', 'Property', ['Green', 'Dark Blue'], 'None', 4, 1],
    ['St. Charles Place', 'Property', ['Purple'], 'Purple', 2, 1],
    ['Virginia Avenue', 'Property', ['Purple'], 'Purple', 2, 1],
    ['States Avenue', 'Property', ['Purple'], 'Purple', 2, 1],
    ['Purple & Orange Wild', 'Property', ['Purple', 'Orange'], 'None', 2, 2],
    ['Tennessee Avenue', 'Property', ['Orange'], 'Orange', 2, 1],
    ['New York Avenue', 'Property', ['Orange'], 'Orange', 2, 1],
    ['St. James Place', 'Property', ['Orange'], 'Orange', 2, 1],
    ['Boardwalk', 'Property', ['Dark Blue'], 'Dark Blue', 4, 1],
    ['Park Place', 'Property', ['Dark Blue'], 'Dark Blue', 4, 1],


    ['Rent - Dark Blue & Green', 'Rent', ['Dark Blue', 'Green'], 'None', 1, 2],
    ['Rent - Orange & Purple', 'Rent', ['Orange', 'Purple'], 'None', 1, 2],
    ['Rent - Light Blue & Brown', 'Rent', ['Light Blue', 'Brown'], 'None', 1, 2],
    ['Rent - Black & Electric', 'Rent', ['Black', 'Electric'], 'None', 1, 1],


    ['Pass Go', 'Action', ['None'], 'None', 1, 10],


    ['Deal Breaker', 'Action', ['None'], 'None', 5, 2],
    ['Double the Rent', 'Action', ['None'], 'None', 1, 2],

    ['$1', 'Money', ['None'], 'None', 1, 6],
    ['$2', 'Money', ['None'], 'None', 2, 5],
    ['$3', 'Money', ['None'], 'None', 3, 3],
    ['$4', 'Money', ['None'], 'None', 4, 3],
    ['$5', 'Money', ['None'], 'None', 5, 2],
    ['$10', 'Money', ['None'], 'None', 10, 1],

    ['House', 'House', ['None'], 'None', 3, 3],
    ['Hotel', 'Hotel', ['None'], 'None', 4, 2],
    ['Water Works', 'Property', ['Water'], 'Water', 2, 1],
    ['Electric Company', 'Property', ['Electric'], 'Electric', 2, 1]

]
