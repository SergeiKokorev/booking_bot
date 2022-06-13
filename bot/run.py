from booking.booking import Booking


try:
    with Booking() as bot:
        bot.land_first_page()
        bot.accept_cookies()
        bot.change_currency(currency='EUR')
        bot.select_place_to_go(place_to_go="New York")
        bot.select_dates(check_in_date="2022-06-13", check_out_date="2022-06-15")
        bot.change_guests(element_count=1,
                        element_id='group_adults',
                        element_css_selector='group_adults_des')
        bot.change_guests(children_ages=[4, 3, 19],
                        element_count=4,
                        element_id='group_children',
                        element_css_selector='group_children_des')
        bot.change_guests(element_count=0,
                        element_id='no_rooms',
                        element_css_selector='no_rooms_des')
        bot.get_search_results()
        bot.apply_filtration(
            star_values=[1, 3, 9],
            sort_by='class_asc'
        )
        bot.refresh()
        bot.save_results()

except Exception as er:

    if 'in PATH' in str(er):
        print(
            'You are trying to run the bot from command line \n'
            'Please add to PATH your Selenium Drivers \n'
            'Windows: \n'
            '\tset PATH=%PATH%;C:path-to-your-folder \n'
            'Linux: \n'
            '\tPATH=$PATH:/path/toyour/folder'
        )

    else:
        raise Exception(er)