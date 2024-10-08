from rental import Rental
from movie import Movie
import logging

class Customer:
    """A customer who rents movies.

    The customer object holds information about the
    movies rented for the current billing period,
    and can print a statement of his rentals.
    """

    def __init__(self, name: str):
        """Initialize a new customer."""
        self.name = name
        self.rentals = []

    def add_rental(self, rental: Rental):
        """Add a rental for this customer"""
        if rental not in self.rentals:
            self.rentals.append(rental)
    
    def get_name(self):
        """Get the customer's name."""
        return self.name
    
    def statement(self):
        """Create a statement of rentals for the current period.

        Print all the rentals in the current period, 
        along with total charges and frequent renter points.
        
        Returns:
            the statement as a String
        """
        total_amount = 0   # total rental charges
        frequent_renter_points = 0
        # the .format method substitutes actual values into the fmt string
        statement = f"Rental Report for {self.name}\n\n"
        header_fmt = "{:40s}  {:6s} {:6s}\n"
        statement += header_fmt.format("Movie Title", "  Days", " Price")
        rental_fmt = "{:40s}  {:6d} {:6.2f}\n"
        
        for rental in self.rentals:
            # compute rental change
            amount = 0
            if rental.get_movie().get_price_code() == Movie.REGULAR:
                # Two days for $2, additional days 1.50 per day.
                amount = 2.0
                if rental.get_days_rented() > 2:
                    amount += 1.5*(rental.get_days_rented()-2)
            elif rental.get_movie().get_price_code() == Movie.CHILDRENS:
                # Three days for $1.50, additional days 1.50 per day.
                amount = 1.5
                if rental.get_days_rented() > 3:
                    amount += 1.5*(rental.get_days_rented()-3)
            elif rental.get_movie().get_price_code() == Movie.NEW_RELEASE:
                # Straight $3 per day charge
                amount = 3*rental.get_days_rented()
            else:
                log = logging.getLogger()
                log.error(f"Movie {rental.get_movie()} has unrecognized priceCode {rental.get_movie().get_price_code()}")
            # compute the frequent renter points based on movie price code
            if rental.get_movie().get_price_code() == Movie.NEW_RELEASE:
                # New release earns 1 point per day rented
                frequent_renter_points += rental.get_days_rented()
            else:
                # Other rentals get only 1 point
                frequent_renter_points += 1
            #  add a detail line to statement
            statement += rental_fmt.format(
                            rental.get_movie().get_title(), 
                            rental.get_days_rented(), 
                            amount)
            # and accumulate activity
            total_amount += amount

        # footer: summary of charges
        statement += "\n"
        statement += "{:40s}  {:6s} {:6.2f}\n".format(
                       "Total Charges", "", total_amount)
        statement += "Frequent Renter Points earned: {}\n".format(frequent_renter_points)

        return statement
