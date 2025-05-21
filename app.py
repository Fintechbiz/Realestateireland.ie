# Function to create SVG for Ireland map
def create_ireland_map():
    return '''
    <svg width="300" height="400" viewBox="0 0 300 400" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M149.5 38C90 76 70 125 73 160C76 195 85.5 226 92 240.5C98.5 255 110 285 131 315.5C152 346 177 365.5 191 375C205 365.5 238 346 260 315.5C282 285 288 255 290 240.5C292 226 298 195 294 160C290 125 209 0 149.5 38Z" fill="#2A7A78" fill-opacity="0.8"/>
        <path d="M149.5 38C90 76 70 125 73 160C76 195 85.5 226 92 240.5C98.5 255 110 285 131 315.5C152 346 177 365.5 191 375C205 365.5 238 346 260 315.5C282 285 288 255 290 240.5C292 226 298 195 294 160C290 125 209 0 149.5 38Z" stroke="#2A7A78" stroke-opacity="0.4"/>
        <path d="M147 130.5C147 130.5 142 137 140.5 146C139 155 145.5 162 145.5 162" stroke="white" stroke-opacity="0.6"/>
        <path d="M170 120C170 120 180 126.5 183 133.5C186 140.5 186 148.5 186 148.5" stroke="white" stroke-opacity="0.6"/>
        <path d="M202 175.5C202 175.5 209 184 209 194C209 204 202 215 202 215" stroke="white" stroke-opacity="0.6"/>
        <path d="M173 230C173 230 179.5 240 180 247C180.5 254 178 261.5 178 261.5" stroke="white" stroke-opacity="0.6"/>
        <path d="M142 249.5C142 249.5 137.5 257.5 136 264C134.5 270.5 136 277.5 136 277.5" stroke="white" stroke-opacity="0.6"/>
        <path d="M117 220C117 220 111 226.5 108.5 235C106 243.5 108.5 251.5 108.5 251.5" stroke="white" stroke-opacity="0.6"/>
        <path d="M118 178C118 178 110.5 191.5 110.5 199C110.5 206.5 112.5 216 112.5 216" stroke="white" stroke-opacity="0.6"/>
    </svg>
    '''

# Function to create SVG for Euro symbol
def create_euro_symbol():
    return '''
    <svg width="80" height="80" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="40" cy="40" r="37" stroke="#2A7A78" stroke-width="3"/>
        <path d="M50 27H34.3C32.5 27 30.8 27.5 29.4 28.5C28 29.4 27 30.8 26.5 32.5H45V37.5H25.5C25.4 38.3 25.4 39.2 25.5 40H45V45H26.5C27 46.7 28 48.1 29.4 49C30.8 50 32.5 50.5 34.3 50.5H50V55.5H34.3C31.5 55.5 28.8 54.6 26.7 53C24.6 51.3 23.1 49 22.5 46.5V46H20V39H22.5V37.5H20V31H22.5V30.5C23.1 28 24.6 25.7 26.7 24C28.8 22.4 31.5 21.5 34.3 21.5H50V27Z" fill="#2A7A78"/>
    </svg>
    '''

# Function to create SVG for check mark symbol
def create_check_mark():
    return '''
    <svg width="80" height="80" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="40" cy="40" r="37" stroke="#2A7A78" stroke-width="3"/>
        <path d="M22 39.5L35 52.5L58 29.5" stroke="#2A7A78" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    '''

# Function to create logo
def create_logo():
    return '''
    <svg width="200" height="60" viewBox="0 0 200 60" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M39 10L55 21V45H47V26H31V45H23V21L39 10Z" fill="#2A7A78"/>
        <path d="M56 19L39 6L22 19V47H34V28H44V47H56V19Z" stroke="#2A7A78" stroke-width="3"/>
        <text x="65" y="26" font-family="Arial, sans-serif" font-size="18" font-weight="bold" fill="#2A7A78">RealEstate</text>
        <text x="65" y="48" font-family="Arial, sans-serif" font-size="18" font-weight="bold" fill="#2A7A78">Ireland.ie</text>
    </svg>
    '''

# Apply custom CSS for perfect styling
def apply_custom_css():
    st.markdown("""
    <style>
        /* Import Google fonts for consistent typography */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Reset and base styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', sans-serif;
        }
        
        /* Define variables for consistent styling */
        :root {
            --primary: #2A7A78;
            --primary-light: rgba(42, 122, 120, 0.8);
            --primary-very-light: rgba(42, 122, 120, 0.1);
            --secondary: #264653;
            --dark-text: #31373f;
            --light-text: #6B7280;
            --light-bg: #F9FAFB;
            --white: #FFFFFF;
            --light-border: #E5E7EB;
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --container-width: 1200px;
        }
        
        /* Main container */
        .container {
            max-width: var(--container-width);
            margin: 0 auto;
            padding: 0 1rem;
        }
        
        /* Header */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1.5rem 0;
        }
        
        .nav {
            display: flex;
            gap: 2rem;
        }
        
        .nav-link {
            color: var(--dark-text);
            font-weight: 600;
            font-size: 1rem;
            text-decoration: none;
            transition: color 0.2s ease-in-out;
        }
        
        .nav-link:hover {
            color: var(--primary);
        }
        
        /* Hero section */
        .hero {
            display: flex;
            align-items: flex-start;
            gap: 3rem;
            margin-bottom: 4rem;
        }
        
        .hero-content {
            flex: 3;
        }
        
        .hero-title {
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--dark-text);
            margin-bottom: 2rem;
            line-height: 1.2;
        }
        
        .hero-map {
            flex: 2;
            display: flex;
            justify-content: center;
        }
        
        /* Search form */
        .search-form {
            width: 100%;
            margin-bottom: 1rem;
        }
        
        .search-container {
            display: flex;
            gap: 0.75rem;
            margin-bottom: 1rem;
        }
        
        .search-select {
            flex: 1;
            padding: 0.75rem;
            border: 1px solid var(--light-border);
            border-radius: 0.375rem;
            color: var(--dark-text);
            background-color: var(--white);
            -webkit-appearance: none;
            appearance: none;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23666' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 0.75rem center;
            background-size: 1rem;
        }
        
        .search-btn {
            width: 100%;
            padding: 0.75rem;
            background-color: var(--primary);
            color: var(--white);
            border: none;
            border-radius: 0.375rem;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s ease-in-out;
        }
        
        .search-btn:hover {
            background-color: #236361;
        }
        
        /* Featured properties */
        .section-title {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--dark-text);
            margin-bottom: 1.5rem;
        }
        
        .properties-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.5rem;
            margin-bottom: 4rem;
        }
        
        .property-card {
            border-radius: 0.5rem;
            overflow: hidden;
            box-shadow: var(--shadow-md);
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
            background-color: var(--white);
        }
        
        .property-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
        }
        
        .property-img {
            width: 100%;
            height: 180px;
            object-fit: cover;
        }
        
        .property-details {
            padding: 1rem;
        }
        
        .property-price {
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--dark-text);
            margin-bottom: 0.25rem;
        }
        
        .property-location {
            font-size: 1rem;
            color: var(--light-text);
        }
        
        /* Pricing section */
        .pricing-section {
            display: flex;
            justify-content: space-between;
            margin-bottom: 4rem;
        }
        
        .pricing-content {
            flex: 1;
        }
        
        .pricing-title {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--dark-text);
            margin-bottom: 0.5rem;
        }
        
        .pricing-subtitle {
            font-size: 1rem;
            color: var(--light-text);
            margin-bottom: 1.5rem;
        }
        
        .testimonial-group {
            display: flex;
            gap: 1.5rem;
        }
        
        .pricing-icon {
            flex-shrink: 0;
        }
        
        /* Testimonial */
        .testimonial {
            background-color: var(--light-bg);
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin-top: 1.5rem;
        }
        
        .testimonial-with-image {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .testimonial-image {
            width: 3.5rem;
            height: 3.5rem;
            border-radius: 9999px;
            object-fit: cover;
        }
        
        .testimonial-text {
            font-style: italic;
            margin-bottom: 0.5rem;
            color: var(--dark-text);
        }
        
        .testimonial-author {
            font-weight: 600;
            color: var(--dark-text);
        }
        
        /* Security section */
        .security-section {
            display: flex;
            align-items: center;
            gap: 2rem;
            margin-bottom: 4rem;
        }
        
        /* Fix Streamlit styling conflicts */
        .stApp {
            backgroun# Function to get base64 encoded images for house thumbnails
def get_house_image_base64(number):
    # Dictionary of base64-encoded house images (ensures images always load)
    house_images = {
        1: "data:image/jpeg;base64,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# Function to get base64 encoded images for house thumbnails
def get_house_image_base64(number):
    # Dictionary of base64-encoded house images (ensures images always load)
    house_images = {
        1: "data:image/jpeg;base64,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# Function to get base64 encoded images for house thumbnails
def get_house_image_base64(number):
    # Dictionary of base64-encoded house images (ensures images always load)
    house_images = {
        1: "data:image/jpeg;base64,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",
        2: "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAoHCBYVFRgVFRUYGBgaGhgYGhgaGBgYGBgaGhgaGRgYGBgcIS4lHB4rIRgYJjgmKy8xNTU1GiQ7QDs0Py40NTEBDAwMEA8QHhISHzQkJCs0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDE0NDQ0NDQ0NP/AABEIALcBEwMBIgACEQEDEQH/xAAbAAACAwEBAQAAAAAAAAAAAAAEBQIDBgEAB//EAEMQAAIBAgQDBQYEBAMFCQAAAAECAAMRBBIhMQVBUSJhcYGRBhMyobHBQlLR8BRicuEjkvEHFTOCliRDU4OTs8LS4v/EABoBAAMBAQEBAAAAAAAAAAAAAAECAwAEBQb/xAAlEQACAgEEAQQDAQAAAAAAAAAAAQIRAwQSITFBEyJRYQUycYH/2gAMAwEAAhEDEQA/APn4Euoj0EKWlLBaUmKaS/3ct92JA7K8kr93L/dyMVAWSSFOFZJzJGCDinKxTlpSQKwBBlpyWFSVlIQBASdtZYFkgkIAZEktZ1UlyU4QUQWXgWkFpSxY6QDDXDuHPiHyJ/MSLC3mTYeU57GcLGHqhqhGe17BgFOt7X3mw9neHLh0NR9ajDfrY/IDxJMyftu5apTS9wEY+bG/yEjkk4pNGxpSk7Mtw3hVauxCI1ueQC/1HYeMfL7M1lIDNTIIv8R+h0nof9nx1xHif/iZuTJf7SRm8Bt1xFMzTex6DfEMfBV+5M1vtRxFKFFhqGe4BI2XS7G4nz/DVKmHfOjWa2YbAi9tteRtDKnRpY20mlxRsnwuGP8A3IXxpj9ZKjS4dV+DEt7o7BtV9T3RcnFa2b/ivfuNvrOs9Vif+I/LlpzMm1D2U7XJUjaJRw+Ivei/+Q2/rrL/AOA4lmCpRc5jYAGx9TKKXFKws3vLgbdhPLYwB+PYwXs6AE2JyqN97FrEwOTCl/hZiUxGGchyabWtlNnQnTY3N4mJ0J6wJeP12NveLt+C9tOWtrww8fr8nS/9A28fKTlEMVJeRYZJZMxR7QVQMoWmbW0yEkDY7W1g+D9pDmAqKADu6i48VOnoYloqlQzZZS6Qt8crWsaaafyi3rqYLVxVN9z6ra/rBXIKaGjJK2SEtiVGzjXoRrK3xCX3t57fOK+A2MLq0pzVKbA3zDU7aSwODKyIrQCqsIyjwj3jvBhUcVKQuDbMnQnmvryhfD+HMzogU5nYKLdTc+mh9ItX0FJvsrp4S8No8LiU4Wva8XwvC2zhNNTa8FhpjR+G2gitbwXEUwCRH4pQL3F4vQXkCRImHtTtLxhtIQtMXlgS0BjzU5E0pYWkSYQHPdy9EM6qy7JAdHnpsqynwlqpJlZAgHJTlgWWIkvWnCYrVJYiR5RpaDYO4gdoQHFV6irTZW0zC1+h5RHxHC51ao17ILA3tpcm3oR5w6qDvF+Ox1uo9YEY2Vw+z7IGfOQ7EtlsPiN/SYjiOCcsdPD9dZ9BwNdchG9iBbmVvcRXxSgudzoAQRfvmcn2KtEueXTTVnzr3DEag28dJNEZTdRbocpI8zpN5i8IlrZVPTQXgdTh1NxZkyHy9RpJXJ0bY9vA/wDZ3Ee+wwYq4am9roQR/iMARfqJLiAwrOc1OnlYKbWS1ttRtMv/AAa03JHYYEXAB1sDqNj3QtvaB6dhhzlY8r3B66RG5fAKl5RXj+EKtMurbXGUaMdDra2/QRdQ4W1MNcq+Yasucaix58/tHbuXBVgT1Fgb+FpTiuGBluGKk9L6+Iv8pXlojJWuTH1nLNmYWY9Bb0tpBw0d1OG5T3c+/wDSUIKKHtFweRTWLdbA6wbkZZmkP4dTQPqaZU3vcNoL9R0mxqcKo1sNUYLkNTLYgCw7NiPOxnyzDY9qTXW3VToQe8Ga32e9oqjuquwfvJAPr3RuNouVJ0zRYHgVCkLKhJGzHU+XQS3E8LRgcoAvvbQ+Y0MvXGBt5dkBgtNglTZj+I8IyaobrvaxU/8A1Mpq4RlOoM3+KoTN8RpWcxtVkZf6Zcsr5FVGhoRGoGe/nMmvJKdA8qT8vvDHqEMFJ1JtY9DvI1MK6jNoRMm7sV7a4DKiG8vTDASFJ7HWHIbSgGaSPiamv71jkprcWkMThoGwWV0DbUyRWWBJPJGAUWkSJeRKyIgKrTocS0JKykJi8NLlaUiJvaXhdOhUABZkqZTqxzKwGl78jYn5QMK6FLrCqCay3LK1pxZJUqJYBXXQwGu2kOrmKcS8jEeXZTVraSunX5whzaK8RiQrXMZyHqzT4Lii5SQSPt9JL2i4k4GRbWvmNh35dP8AMB5RFwypcsSDmFxYnTv9ZRxZs+JbNsdP8qjN8gZK2pciJwklQtp8RYUw7WYk5QuxGlidNu/vgSYq7kAC3MX1v+9YNh8STnptc3BKjp0HmBJ0DYa93f0lk/kh6fxbIugGt/UmD47DZgbakMDrCPcrGmLChAKamzNfM9/wg7KO/n4QVcOt2DwjAfidmXwEaEE+QYy4Ql4d2Ky37JJ8QLwSrT7RNufzM9XQB30GY3HlsR5ix9ZW72GnYufPXmDYnrbUSiaXCIbm3bFb0+sHqUhyjZ8KOh/8vyI18LQV8D0P76Sr/wAION9P9gFpNWjJMCt5OjiCjBhCUpD+X0/tJphwevry0/WCzJhIcML7S0UzLKVBR1g1WsOpES2WjSHdKmBK2aNaeFshPSLnpQbgSZT7uGVKWkWLWhnvrmCwo9TeGO8URuMWQjK3x90R4pzKSIWmzpEK4ZiAjgn4WGVu7kD5aHylDBQ56YkAkOwWQAjWI3RxjLRTnbSdEYMNt0TRIfQp2iJI/wCH6qZ2Vp047JZjWwTEGK8TUteElY4oPeKmW3KCX0aNWzLcQR2NlJ87WiamubRkYE7ppp4zdVfZdCpcPUXXQAt/+ZVwvgC0XuGLZu0SpFhu1r7HUff144Jppmji2IcpYzC8Ept/FKT0c+BspA+c3qOoPYGm+YnXb8o58yR42ip6KK61GB7Z1ufiBOvlrLY37f8AQ5I+7+hWGpZEVf5RCRSheCwxdVYLoV18BL6bXl5STI4p5PYpfsBakACu3ePrJVYVTMUU06aPDVTM7xgZ0RkNirA5vHl8wZpKRitaIFdqbd2jDx2PmD84I3fBTJFumDcZ4eQQwY62N7f20mdrUQDoQe47H0m04lhLKGSxJN1G2bvXx5jnM3xKnqHQrUUab7cuokvVnFdFXpsOR+2Qqp9zVlFxqD0I1B8ZCpTt3yumhVgVJB6jQy97EXFLkrPCKksqCQWnCnF0KysrDKGDB7W6axbiMEw2lqYhwUJuQCLdZdE5pQb7BKmFB5Qd8PDQJzLAn0Gt5Y5D02EY8PxYAyk9reNVMT0cNcA7wi00HFMPn7Q0zD0MRUtLQJcm0Y3hl7NPXFPI1HaWvXJb1Eckhs/GFFTIi0Z4HCZhaU4dQGvLaFSzRKKtrLBpLKplKCE0qUaKtiTwSytG+AwIyzM8cw+V7y2KScXJk5ZKTZdgk0ly1NZXTktJJTlLM2brhfEAzaQnEYVX1mY4VjMj98fUcXeJLG0xZRaYs9ocJlUMv4dP6fynyt8plcYg29fSbbjFcOjIdwb9+nP0mQxiHW20WSo0H7RNQ7I9ZYryvF0S7WMIppMmJLswXIbTtK8HxFkv0EMw9S+kLJzXCYzo1MzAjnp56feU1DH/ABrhi47aDUaen9/rE1XDkdLyL4dMaM1JeR/gqgbSMFxKGZlKrLvG+CxF5TaRdvsSJVtYsxlPfv1jUm+v7vF9ZJKaKOVGc4g1soHjKcWnaT+n7QvH08zesrajeooQD4iFHm3XxUaeM8vqVyerD2qjLVqYlNvAnpf9fpHGKwpcXF46oYYZctgQNIPnSo7NVyxRwzF3BAMcnhwdfcufd1f/AAnPwVD+BvyOfyt6Gxq4f2mwtPNTKtSqLo6uDkYHnY/Qg+s5wThYx9VqSuoqZfeI7DssV2A5MCdtYb/Jy3M508PD+TGtUNM5XBVhvflK1p9pm340nD6iYZKYo1qwZkzaFqbDZle2+psbAaHScxnD6FdxUsKVZmHvEH+G+b8TD8Lde6XjnnH+iDwRfHaPm3EFCNptJhXEMpvoQQR1BGoPpfziNxNLLxl0RqUpUekCSOpHLx0mL0qwtxvDqVJtDXtM2rBoVIJY0uwVa0GxzAmFfodLYN8Z77TyG8mVnQZ1QQOAcynxnibxfQpkm1o3OGKjTlIp+4eSXEzNUnKLRovDpBUEaZ3JWLj4FHcJwXCqLxhWpSjDtaTxytlZyvk5TpRVxbD6XjRKkGx9O4jZHuRPHJEaAuLGNlp3vKanDRLVwt4uxqMk0ZrjVM9lh4HxmUx6ZWOul+XQ8vWNOJ4kqxXlr46xfxAB8p5hffv8z1j21wd2TlWQ9h8QLX+sYI0yvDK+Qkfy8z8o7oOGF9v9eUmym12aHh7i1oRjHUi376RLga9iPnL8dXuDIz7IZMaMpjQJUj2uD6QfGYzULz5+Z5xRXxZvKmry6SR0YkobmF42qLrbzPnJVzdVtt2h+sWvVncPUzLGlBRl/TaHD3NvopTDlibS9MOAItw78obUrQNFFfImGHuTrJrhLm0jgn1EfYHG2GsJCbv3FHxTEZOZwIvnfXrF+NxZOmunzlOMcZvP1nMVRJsRzLfeNGFr+k5StlvDzfEW/cj5f2msw5slvD95Zh+DcPOIdmIvZhfwKj7mfTuGeyrvlvVCJ+RQGb/Mfh9b+EmklyzOTnNK+BPgMN72uAVYFsqqVN1zMwUMOoBIv3CbDC+yIVSUPa3L9/QCxP3j7hOAp4dAlNbfmY6u3ex5dwsI1YyyXgzl47GPBvZxaJ94VVqo+J9SR/KoOwHfvqY5FLW/72jtm/d4Bi6AAJbQAXJ6SbHhExVD1K1mF+YOngRczAe3PswpU4qmuVzZag2z9A38481Pbm1peyeJ/iC6vfo9vwg6GXY8zhK+iTxKa47PiNI2k3XUeM03tRwBkbtKRlaxvyPQ94PrMxkDzpk7WziStUBUoUFhVXDkHSdp0YyYKFaJLjwvE4e0XVDYxrjXlAQSICNobhMOXMAW5jXAoTvI5cqXCNGN8sGOGYSlqRJt6QnE9IH79lJ79/ScuSbfLMo3IJQ2ldN4O1SxvCMHT7VzyhSsZy2uxwDFmOIJjOBYqnC4lY00zLewI7nOH0LEwlKsrx9MZY0vdFsF41ZBWF7CL+K4mw8RGq0riZ/j1Mg2HPcwSgm2dvU1EQVb32g1TEkSmrVv5QKrXA+cWOOzgWJyDHrltkPVyecXcRe7HLzMnUpXsJZ/CaXlNyUThko+p8iihhO1qYz4JwotYsuxsJdxPAs2iKSBuQJNY5Xwi2R3zEQrVzLrFmLbKfKO+H4Rl3JHdrLcThQRpG2tLkCklxwI8BWzjKJp+HcLK6lZRw3gDFrsBl6nT+/lN3wrhyUxZVueZOphmqXBPN6aSVRf9KOH4GwuRH9HDgCwFhygaU9YciBRL8HBKW5ijF8O+Iwkk6wNsUiG9xcctYwxtyukyPa6eTRtR4GnD+FpTFgN92PMw/KJ7NeXBbympKkkqQm7dpk2AE+fVuIvVqOxuVa9r9ygeQnluU2BuxOrnRV8r9oeZ8IHxnFdkqvM2+QieKTk1HskrXTG2PxarTBY2ttqbC+l7HX5Qr2YwuYvXPIe7X/LZm9coH+aIuGYZqtQITZFPve7T4Aeua49L8po8Tie0qqQVXK6KLa2C51H9IB15luQnoKPtORLlnPeLtvfHRuMPsvjeWVdYJhagZQw2IBHgReWuZ2nnRLLmB9R9ZhuN8Iyu63HYbOp6FRnPzE3JP78YDxXCCrRqJ1Rl81IYfMCXwS2y+iGVXH7PnSIEt0lGMphrg7jT1nKrkiT9/wAU9CUbRwxfgTY/EWGkaYWl3ReD7x5hqenKc2WbXBXFxyyVPCX0Ih+H4RmExvsMPkXl8HI2AJ9I8WSVcDShHy0ynF8HZDO0PZ17a8o8x9MWAy8xGFXCBU02tB6lS5CsMWrAK7kDSdwb5lIlmIp313tCMDhAgvsT9ohqHnCl6SlZXRqZyYRiUFz4wFadmtGi2pNsn69OkkJ8OgvluO8GQemNxzNrwUU3Rl06kHxlrUiOa+n6xZrci8NrkjO4N+0QeVzA6uOsbqfCd91UXOloWiAG4EpniRXDF7mZTE4i7y1DaFY7DC9oLRpEbzpjJUceScXIHZ5XWqaRk2Hc8tJPDcO0BJvJzyRXR146ZRwrCFX7SluzpNDQpX1MhSoAC0PVLSEpuTKc6QJTp2hAEsKSJFpNInQXhHlNCW2noEFhDwJwLJz0KAyulTEsMrZpgBFFtpXUVTqRLhTvOVB3QWAyWM9lM7NXoWzBxnQc9rfKwHTuEzPGeCnDuCdRtmG48RzE+oYml8p8t9saz9tSfhUAAanrsdZP1K4GPfufyDezi1CzVn+FM2XvZiEF/K/zmq4vSyOuUBUyKUXQntKUuTqSbn1MQ+xtFSSxUEE5AdD8K639TG/ETd+l3J8z18rkeMeUduNvtss8bXA64Kf8Cj/QP/zNNjnmNwWJ7FEf9NJq8RVuJ3ZPyRxYZ8DGqZXmbmh9SBPIwzD8ofvuJHzm6oG6Zn/aHCinVDp8FM3XxDNr65/UTJ1KS7W0NvUWP1BM+hcYwvvKZW1yL2vyI1mdpYIN8aqfHL9LKfQSM7Uk0NDJjywakrTM/iMVWFgwZhyBACjyGg9JXR4q6bqw8R9xNZS4cRpdR3C56/vSMKPC3qHtqtr7ra/nfS/zm9OEVcrZB6ic+IL+GB/3s/cPAmE0w7/Ep81H1vNcnsfTO9RiO4LP1eFp7PUF3VifFifrCssF0jKGRO3ZjEpP1f8A7v7SavfZGP8AlH3m0Tg1EfgG/eLnzOpiziWCQYYhFGZmRBpqAzBb9+l4Y5YtXQMmKSdJM+e1kdtyE82W/wBohemxcgHMD0BNtRN1V4RRXD# Function to get base64 encoded images for house thumbnails
def get_house_image_base64(number):
    # House images encoded as base64 strings (ensures images always load)
    house_images = {
        1: "iVBORw0KGgoAAAANSUhEUgAAAQMAAADCCAMAAAB6zFdcAAAAe1BMVEX///8AAAD7+/vx8fH09PT39/fv7+/o6OiIiIjo6OW0tLSamprj4+Pd3d3Pz8/Hx8fV1dWfn5+rq6uSkpJ+fn7AwMBvb29nZ2dXV1dPT09GRkY8PDw0NDQsLCwjIyMaGhoQEBAJCQlgYGBycnKMjIx5eXkkJCQWFhYxMTE7NXcnAAAKeElEQVR4nO2dCZuiOhCFIYGwyL6IgCs6rf//F77E7nb6dYtAEs3MnO+ZfpSGEA6VpCoL8fEBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPxK4iR7UZLFcfS3n+c/JEnD7MXcZknyt5/ov0Ae6l7TNOV5SZoVZVXVdd00TZ5nSfy3H+2/QJj5SjE1+e6dc9XvZ45YVeVZBU/9Nom55hVP7fddZDW3vAHx336ufw1RTJXn7e6rdvfHuW/Bt/34KNaRaK1gMM2oHesrXMumCIK/8oj/JJkwE+35yvDDO52Pjm1b9d9+vn8NmVTKcO8+4HbxsmnVUfm3H+3fJJadqPl3Ofj1+Ntl7cvzb83L/TjpdJz71g5EFXQVL+g1xxpk+bff5Z9BPnHy3AV8YGpOljjpM55/8T3yU/G5k7KOmTK7eTmBvbXGwVz8yoP//kJmNlfK3qzqh/cVphH2N7v7lYOdeLVpvstdvnFKKLnM0jtU+9zXC1c+8tXwFe/3OVIpOYr38NSVFKV/+4X+OZqDsBi97hpL+eH9pS/5Wn2bQywlbSfbHUFzKH7AKwlD7/dlEOl7qQMnJtX8YW1B0p5+pRPXxKL2DvMEQwn/uD+SxYFOJGTg+1X/+1RqjU4G66KORMuAb3PpdzrjdKaGBwPuHH07LHgwLLRJByVKb6MQfFpkPVKcaVMJsS3X9TspdPGTh9PVvnegfG0XLRBqyfQJCbA9k34MaymMMhCjE1H9yqZVQw7rA+HGGKWEupWSVmTSOocnc3dO0mjFcqEiB8PgXrg8j5e/+zyLVgolXm82Noc4NZLDWD3YlhNmGnUQlPrNlimport streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import base64
from io import BytesIO
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(
    page_title="RealEstateIreland.ie",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------------
# Image helper functions
# ----------------------

# Encode house images to base64 (used as fallback if external images fail)
def get_base64_house_images():
    # Dictionary of base64-encoded house images (used as fallbacks)
    house_images = {
        "house1": "data:image/jpeg;base64,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
