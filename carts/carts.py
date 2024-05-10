from courses.models import Course


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.request = request

        cart_session_id = "cart"
        # get the current session key if it exists
        cart = self.session.get(cart_session_id)

        if cart_session_id not in request.session:
            # save an empty cart in the session
            cart = self.session[cart_session_id] = {}

        # make cart available in all pages
        self.cart = cart

    def add(self, course):
        """Add a course to the cart"""
        course_id = str(course.id)
        if course_id not in self.cart:
            self.cart[course_id] = {"quantity": 1}

        self.session.modified = True

        # Deal with logged in user
        # if self.request.user.is_authenticated:

    def get_courses(self):
        # get course ids from cart
        course_ids = self.cart.keys()
        courses = Course.objects.filter(id__in=course_ids)
        return courses

    def calculate_totals(self):
        """
        Calculate the total price, total discount price, and total regular price of cart items.
        Returns:
            Tuple: A tuple containing three values - total price, total discount price, and total regular price.
        """

        course_ids = self.cart.keys()
        courses = Course.objects.filter(id__in=course_ids)
        total_price = 0
        total_regular_price = 0
        total_discount_price = 0

        for course in courses:
            if course.discount_price is not None:  # course has discount
                total_price += course.discount_price
                total_discount_price += course.regular_price - course.discount_price
            else:
                total_price += course.regular_price

            total_regular_price += course.regular_price

        if total_regular_price > 0:
            total_discount_percentage = round(
                (total_discount_price / total_regular_price) * 100
            )
        else:
            total_discount_percentage = 0

        return (total_price, total_discount_percentage, total_regular_price)

    def delete(self, course):
        """Remove a course from the cart"""
        course_id = str(course)
        # delete course id from cart/dictionary
        if course_id in self.cart:
            del self.cart[course_id]

        self.session.modified = True

    def __len__(self):
        return len(self.cart)
