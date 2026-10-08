# Project Context — Restaurant Pickup Ordering System

This document is the persistent source of truth for AI assistance and human contributors. Prefer this file over chat history when deciding what to build next.

---

## Project purpose

Build a web application that lets customers browse a restaurant menu for pickup ordering, and lets restaurant owners manage that menu. The long-term product supports browsing, a cart, and pickup orders. The catalog stage is complete: Django foundation, product catalog, customer menu view, and owner product management. The session shopping cart stage is also complete: add, view, quantity changes, remove, quantity limits, and progressive-enhancement JavaScript. The next product stage (checkout / orders) remains out of scope until explicitly requested.

---

## Technology stack

| Layer | Choice |
|-------|--------|
| Language | Python |
| Framework | Django |
| Database | SQLite |
| Templates | Django templates |
| Front end | HTML, CSS, JavaScript |

Do **not** introduce React, other SPA frameworks, or separate API-first clients unless explicitly requested.

---

## Users

### Customer (no account required)

- Browse restaurant products on a menu page (implemented)
- Add a product to a session cart and view that cart, including image, name, unit price, quantity, line total, and cart total (implemented)
- Increase or decrease quantity, set quantity via update, and remove a product (implemented)
- Order between 1 and 20 units of a single product (implemented; server-enforced)
- Future: place a pickup order

### Restaurant owner (authenticated)

- Authenticate (log in / log out)
- Add, edit, and delete products

---

## Catalog requirements (implemented)

1. Django project setup with SQLite and Django templates
2. Product database model with: **name**, **image_url**, **description**, **price**
3. Five sample products seeded in the database
4. Customer-facing menu page that displays products
5. Owner authentication
6. Owner product CRUD (create, read, update, delete)

---

## Catalog stage scope (implemented)

**In scope for the completed catalog stage:**

- Project scaffolding and configuration
- Product model and migrations
- Sample product data (five products)
- Public menu page (read-only product listing)
- Owner login/logout
- Authenticated owner flows to manage products

**Assumptions for this stage:**

- Single restaurant / shared product catalog (no multi-restaurant model)
- Owner uses Django’s built-in authentication (or equivalent simple auth)
- Product image is a publicly accessible **URL** stored in `image_url` (`URLField`), not a file upload. Classroom demo only; no `ImageField` or media storage.
- Menu is viewable without login; product mutations require an authenticated owner
- One owner role is sufficient; no fine-grained permission matrix beyond authenticated owner

---

## Out-of-scope features

A session shopping cart is in scope for the cart stage (now complete). Do **not** implement the items below unless explicitly requested later:

- Checkout
- Ordering / order placement
- Payment
- Delivery
- Customer registration or customer accounts
- REST/JSON APIs
- React or other frontend frameworks
- Multi-restaurant support
- Delivery tracking, notifications, reviews, or loyalty features

---

## Important design constraints

- Server-rendered pages with Django templates; progressive enhancement with CSS/JS only as needed
- Persist products in SQLite via Django ORM
- Protect create/update/delete behind owner authentication
- Keep the data model minimal: product fields are `name`, `image_url`, `description`, `price`
- Prefer clarity and teachability over premature abstraction
- Avoid adding apps, dependencies, or patterns that are not required by the current scope

---

## Naming conventions

| Kind | Convention | Examples |
|------|------------|----------|
| Django apps | lowercase, short, singular or clear domain name | `menu`, `accounts` |
| Models | PascalCase, singular | `Product` |
| Model fields | snake_case | `name`, `image_url`, `description`, `price` |
| Views / URL names | snake_case | `menu_list`, `product_create` |
| Templates | snake_case, descriptive | `menu.html`, `product_form.html` |
| Static files | descriptive paths under `static/` | `css/menu.css`, `js/menu.js` |
| URLs | kebab-case or short path segments | `/menu/`, `/owner/products/` |

Prefer consistency with Django defaults when a convention is not specified above.

---

## Development principles

### 1. Implement one small feature at a time

Complete and verify a single vertical slice (model, view, template, or auth piece) before starting the next. Prefer incremental, reviewable steps over large mixed commits of unrelated work.

### 2. Do not introduce features that were not requested

Do not add checkout, orders, payment, APIs, extra models, or “nice to have” behavior because it seems useful later. Stay within the catalog requirements and the shopping-cart stage below.

### 3. Explain significant design decisions

When choosing among valid approaches (e.g. app layout, image storage, auth wiring), briefly record **why** in commit messages, PR notes, or a short comment in this doc—so future AI and human work can stay aligned.

---

## Catalog stage acceptance criteria (complete)

This stage is complete:

- [x] Django app starts successfully (e.g. `runserver`)
- [x] Product model includes name, image_url, description, price; migrations applied
- [x] Five sample products exist and are usable
- [x] Customer menu page shows all products with those fields
- [x] Owner can authenticate and access product management (Django admin; superuser `quick_byte` exists)
- [x] Owner can add, edit, and delete products; changes appear on the menu
- [x] Unauthenticated users cannot create, edit, or delete products
- [x] Out-of-scope features above are absent

---

## Current Development Stage: Shopping Cart

Approved on 2026-10-01. **Complete** as of 2026-10-06. The catalog and owner flows stay as they are. Cart mutations remain session-based; checkout is still out of scope.

### Implemented for this stage

- Django project, `Product` catalog, five sample products, public menu at `/`, and owner product management in Django admin
- Customer can browse the menu without an account
- Add a product from the menu into the session cart. A second add of the same product increases its quantity by 1 (until the per-product maximum). New products start at quantity 1. The action is POST-only and redirects to `/`
- Cart page at `/cart/` shows image, name, current unit price, quantity controls, line total, and overall total. An empty cart says “Your cart is empty.” and shows `$0.00`
- Increase quantity by 1 (`POST /cart/increase/<product_id>/`) and decrease by 1 (`POST /cart/decrease/<product_id>/`). Decreasing a quantity of 1 removes that line
- Set an absolute quantity with `POST /cart/update/<product_id>/` and form field `quantity`
- Remove a product completely with `POST /cart/remove/<product_id>/`
- Per-product quantity must be an integer from **1 through 20** (`MAX_CART_QUANTITY = 20` in `menu/views.py`). Server rejects 0, negatives, non-integers, and values above 20 without corrupting the session. Add/increase do not raise a line above 20
- Progressive enhancement: `menu/static/js/cart.js` adjusts the quantity input on +/- and submits the update form. Without JavaScript, +/- / Update / Remove still work as normal POST forms. JavaScript does not calculate authoritative prices
- Customer navigation on the menu and cart: QuickBite | Menu | Cart, with the total item count beside Cart
- Five tests in `menu/tests.py` for product creation, the menu page, and anonymous admin access. They do not cover the cart

### Cart rules (keep supporting)

- The cart is session-based. It exists only for the customer’s browser session. Store product identity and quantity in the Django session. Do not add a cart table. One line per product: adding a product that is already in the cart increases its quantity. The displayed price is the product’s current catalog price. The total is the sum of price × quantity for each line. Use decimal prices, not floats.
- Customer login is not required. Adding, viewing, and changing the cart works for an anonymous customer.
- Checkout and permanent orders remain out of scope. Do not implement checkout. Do not create `Order` or `OrderItem`. Do not collect pickup information. Do not implement payment.

### Future features

Still postponed:

- Checkout, order placement, and saved orders
- Pickup details
- Payment
- Delivery
- Customer registration or customer accounts
- REST/JSON APIs, React, multi-restaurant support
- Delivery tracking, notifications, reviews, or loyalty features
- A custom owner dashboard

### Acceptance criteria

- [x] From `/`, adding a product and then opening the cart shows that product’s name, price, and quantity 1
- [x] Adding the same product again shows quantity 2 and a total of price × 2, still as one line
- [x] Adding a second product shows two lines, and the total is the sum of both lines
- [x] Increasing a line’s quantity by 1 updates that quantity and the total. Decreasing it by 1 does the same
- [x] Removing a product drops that line, and the total no longer includes it
- [x] An empty cart shows no product lines and a total of `$0.00`
- [x] A new browser session starts with an empty cart. Another session’s cart is unchanged
- [x] These actions work with no customer login
- [x] The application has no checkout, pickup form, payment step, `Order` model, or `OrderItem` model
- [x] A customer may order between 1 and 20 units of a single product (server-enforced; quantity 1 and 20 accepted; 0, -1, and 21 rejected)

---

## DEVELOPMENT STATUS

Snapshot of the repository as of 2026-10-06. Treat this section as the handoff for a new session. Prefer the code if it later disagrees with this section.

### 1. Completed Features

Implemented and verified:

- Django project `restaurant_system` (Django 6.1.1) with SQLite at `db.sqlite3`
- `menu` app listed in `INSTALLED_APPS`
- `Product` model: `name`, `image_url`, `description`, `price`, plus `__str__`, a minimum price of 0.01, and check constraint `product_price_gt_zero`
- Migrations `menu/migrations/0001_initial.py` and `0002_alter_product_price_product_product_price_gt_zero.py` applied
- Fixture `menu/fixtures/products.json` with five products (primary keys 1–5). The live table also has five rows. Two live prices differ from the fixture: Chicken Wings is **10.49** (fixture **11.49**) and Chocolate Milkshake is **7.49** (fixture **5.49**)
- Public menu at `/` (`menu_list`): title QuickBite, heading Our Menu, one card per product with image, name, description, dollar price, and an “Add to Cart” POST form. Renders all five products
- Session cart add at `POST /cart/add/<product_id>/`. A missing product returns 404. GET returns 405. A new product is stored as quantity 1; adding it again increases that quantity by 1 up to 20; at 20 further adds leave the cart unchanged and still redirect to `/`
- Cart page at `/cart/` (`cart_detail`). Each line shows the current image, name, unit price, a quantity input (`min=1`, `max=20`), +/- controls, Update, Remove, and line total. The page shows the overall total. An empty cart shows “Your cart is empty.” and `Total: $0.00`. A product id in the session with no matching row is omitted from the lines and the total
- `POST /cart/increase/<product_id>/` (`cart_increase`): +1 when the line exists and quantity is below 20; redirects to `/cart/`. Missing product 404. GET 405. Corrupt/non-positive stored value for that key is removed
- `POST /cart/decrease/<product_id>/` (`cart_decrease`): −1 when quantity &gt; 1; at quantity 1 deletes the line. Redirects to `/cart/`. Missing product 404. GET 405
- `POST /cart/update/<product_id>/` (`cart_update`): sets absolute `quantity` from POST when the product is already in the cart and the value is an integer from 1 through 20; otherwise leaves the cart unchanged and redirects to `/cart/`. Missing product 404. GET 405. Not-in-cart is a safe no-op redirect
- `POST /cart/remove/<product_id>/` (`cart_remove`): deletes that session key if present; safe no-op if absent; does not require the product to exist in the database; redirects to `/cart/`. GET 405
- Quantity validation helper `_positive_quantity` / constant `MAX_CART_QUANTITY = 20` in `menu/views.py`. Invalid quantities (0, negative, non-integer, &gt; 20) are not stored
- Progressive enhancement script `menu/static/js/cart.js` on the cart page: +/- update the quantity input and submit the update form (decrease at 1 still uses the decrease form to remove the line). Prices and totals remain server-rendered
- Customer nav on the menu and cart pages: QuickBite | Menu | Cart (n). `n` is the sum of positive session quantities from `menu.context_processors.cart_item_count` (does not verify that each product still exists)
- Stylesheet `menu/static/css/menu.css`, served at `/static/css/menu.css`. Responsive card grid and cart quantity control styles
- `Product` registered in Django admin (`ProductAdmin`: columns `name`, `price`, `image_url`; search on `name` and `description`)
- One superuser exists: username `quick_byte` (`is_staff`, `is_superuser`, `is_active`)
- Anonymous requests to `/admin/`, the product changelist, add, change, and delete URLs redirect to `/admin/login/`
- Owner add and delete were confirmed on 2026-10-01 as `quick_byte`. A temporary product appeared on `/` and was then removed
- `python manage.py check` reports no issues (re-checked 2026-10-06)

### 2. Current Architecture

- **Django project:** `restaurant_system` (`manage.py` at the repository root, next to `docs/`)
- **Apps:** `menu` only (plus Django built-ins: admin, auth, contenttypes, sessions, messages, staticfiles)
- **Models and relationships:** one model, `menu.Product`. No foreign keys. No cart, order, or custom user model. Owner accounts are `django.contrib.auth` users.
- **Product fields:** `name` `CharField(max_length=200)`, `image_url` `URLField()` (default max length 200), `description` `TextField()`, `price` `DecimalField(max_digits=8, decimal_places=2)` with `MinValueValidator(Decimal('0.01'))`. Check constraint `product_price_gt_zero` requires `price > 0`. `__str__` returns `name`.
- **Views:** `menu_list` loads `Product.objects.all()` and renders `menu.html`. Cart views: `cart_add`, `cart_increase`, `cart_decrease`, `cart_update`, `cart_remove` (all `@require_POST`), and `cart_detail`. Helpers: `_session_cart`, `_positive_quantity`, `MAX_CART_QUANTITY`. `cart_detail` loads products with `in_bulk` and passes `lines` plus `total`. Each line dict includes `product_id`, `name`, `image_url`, `price`, `quantity`, `line_total`. Money uses `Decimal`, quantized to `0.01`.
- **URLs:** `restaurant_system/urls.py` mounts `/admin/` and includes `menu.urls` at `''`. `menu/urls.py` maps:
  - `/` → `menu_list`
  - `/cart/` → `cart_detail`
  - `/cart/add/<int:product_id>/` → `cart_add`
  - `/cart/increase/<int:product_id>/` → `cart_increase`
  - `/cart/decrease/<int:product_id>/` → `cart_decrease`
  - `/cart/update/<int:product_id>/` → `cart_update`
  - `/cart/remove/<int:product_id>/` → `cart_remove`
- **Templates:** `menu/templates/menu.html`, `cart.html`, and `nav.html`. `TEMPLATES['DIRS']` is empty and `APP_DIRS` is `True`. Both customer pages include `nav.html`. Cart page loads `js/cart.js` with `defer`.
- **Static files:** `STATIC_URL = 'static/'`. CSS is `menu/static/css/menu.css`. JS is `menu/static/js/cart.js`. No `STATICFILES_DIRS`.
- **Session usage:** `SessionMiddleware` and `AuthenticationMiddleware` are installed. The cart is `request.session['cart']`, a dict of product-id strings to integer quantities in 1..20. Admin login uses Django’s session separately. `menu.context_processors.cart_item_count` adds `cart_count` to every template as the sum of positive integer quantities in that dict (without checking product existence or the 1..20 cap for display filtering).
- **Forms:** no app `forms.py`. Menu and cart use plain HTML POST forms with `{% csrf_token %}`. Admin builds the product form from the model.
- **Admin functionality:** default admin at `/admin/`. `menu/admin.py` registers `Product`. Add, change, and delete are the built-in admin pages, limited to an active staff user. There is no custom owner dashboard.
- **Other:** sample data is a fixture, not a data migration. `DEBUG = True`, `ALLOWED_HOSTS = []` (local `127.0.0.1` still works while `DEBUG` is on). `SECRET_KEY` is the default development key in `settings.py`. Django 6 `MAILERS` uses the console email backend.

### 3. Important Design Decisions

Do not reopen these unless requirements change:

- **One app (`menu`).** Catalog, the public menu, cart, and admin registration stay in `menu`. Do not add an `accounts` app for this stage.
- **Owner management is Django Admin.** Do not build a custom owner dashboard, login page, or product form unless explicitly requested. Login and logout are `/admin/login/` and the admin logout.
- **Project name `restaurant_system`.** Chosen at initialization. Keep it.
- **Public menu URL is `/`,** URL name `menu_list`. Do not move it to `/menu/` unless requested.
- **Cart URL is `/cart/`,** URL name `cart_detail`. Mutating cart endpoints are POST-only with CSRF: `cart_add`, `cart_increase`, `cart_decrease`, `cart_update`, `cart_remove`.
- **Image is a URL, not a file.** Field name is `image_url` (`URLField`), for classroom placeholder images. Do not switch to `ImageField` or media uploads.
- **Price is `DecimalField`.** `max_digits=8`, `decimal_places=2`. Do not use `FloatField`. The template prefixes the stored value with `$`. The smallest allowed price is 0.01: zero and negative prices are rejected by `MinValueValidator` and by the database check `product_price_gt_zero`.
- **No extra product fields.** No availability flag, timestamps, categories, or uniqueness constraint on name unless requested.
- **Sample products live in `menu/fixtures/products.json`.** Reload with `python manage.py loaddata products`. That reload overwrites rows with the same primary keys, including later admin edits (it would set Chicken Wings back to 11.49 and Chocolate Milkshake back to 5.49).
- **Presentation stays in CSS plus optional progressive enhancement.** Styles are `menu/static/css/menu.css`. Do not add a CSS framework. Cart mutations are server-rendered POST forms. `menu/static/js/cart.js` only enhances quantity controls; it must not become the authority for prices, totals, or quantity validation.
- **Cart is a session dictionary, not a model.** `request.session['cart']` maps a product primary key string to an integer quantity from 1 through 20, for example `{'3': 2}`. Do not store name or price in the session. Look them up from `Product` when rendering so the cart shows the current catalog price. Do not add a cart table, `Order`, or `OrderItem` unless checkout is explicitly requested. The nav count is the sum of positive session quantities, provided by `menu.context_processors.cart_item_count`.
- **Per-product quantity cap is 20.** Enforced in `menu/views.py` (`MAX_CART_QUANTITY`). The quantity input may expose `min`/`max` and JS may respect the range, but the server remains the only enforcement that matters.

### 4. Current Business Rules

Enforced by the `Product` model:

- A product requires a name (max 200 characters), an image URL, a description, and a price
- `image_url` must be a valid URL (max length 200)
- Price is stored as a decimal with two places and at most eight digits (up to 999999.99), and it must be greater than zero (at least 0.01)
- Display name of a product is its `name`

Enforced by the menu, cart, and admin:

- Anyone can view the menu at `/` and the cart at `/cart/`. Neither requires customer login
- The menu lists every `Product`. Each card can add that product to the session cart
- Adding a product that is already in the cart increases its quantity by 1, up to 20. A product that is not yet in the cart starts at quantity 1. There is one session entry per product
- A customer may order between **1 and 20** units of a single product. Values outside that range (including 0, negatives, non-integers, and 21+) are rejected and must not be written to the session. Add and increase do not move a line past 20
- Decrease by 1 updates the quantity; decreasing from 1 removes the line so zero is never stored
- Remove deletes the entire line for that product id
- The cart displays the product’s current database price. Line total is price times quantity. The cart total is the sum of the line totals
- A session product id with no database row is not shown and is not included in the cart total
- Creating, editing, and deleting products is only through Django admin
- Those admin pages require an authenticated, active staff user. Anonymous requests redirect to the admin login page
- The admin list shows name, price, and image URL, and searches name and description

Not enforced: unique product names, a custom owner role beyond Django staff/superuser, and dropping a deleted product’s id from the session. A deleted product’s quantity can still be included in `cart_count` even though the cart page omits that line.

### 5. Verification Status

Re-checked on 2026-10-06:

- **Django system check:** no issues (`python manage.py check`)
- **Automated tests:** `menu/tests.py` has 5 tests. `python manage.py test menu` passed: valid product create, menu HTTP 200, menu shows database products, product name is rendered, anonymous `/admin/` redirects to login. No cart tests exist
- **Database:** `Product.objects.count()` is 5: Classic Cheeseburger 9.99, Chicken Wings 10.49, Chicken Momo 10.99, French Fries 3.99, Chocolate Milkshake 7.49. `auth_user` has one row, `quick_byte`
- **Cart quantity rule (manual via test client):** `cart_update` accepted quantity **1** and **20**; rejected **21**, **0**, and **-1** (session unchanged). Increase at 20 and add at 20 left quantity at 20
- **Cart mutations (manual via test client, earlier in this stage):** increase/decrease update quantities and totals; decrease from 1 and remove clear lines; empty cart shows “Your cart is empty.” and `Total: $0.00`; GET on mutating cart URLs returns 405; missing product ids on add/increase/decrease/update return 404; remove of an absent id is a safe no-op
- **Progressive enhancement:** cart template references `js/cart.js`; static finder resolves `js/cart.js`; without JS the POST forms remain present
- **Admin protection (from 2026-10-01):** unauthenticated admin URLs redirect to `/admin/login/`; owner add/delete of a temporary product was confirmed as `quick_byte`

### 6. Known Issues / Limitations

- If an owner deletes a product that is still in a session, the cart page skips it, but the id stays in the session and `cart_count` still includes its quantity. Increase/decrease/update for that id return 404, so the UI cannot clean the orphan except via a crafted `cart_remove` POST
- No automated tests cover add-to-cart, increase/decrease/update/remove, the 1..20 quantity rule, line totals, or the nav count
- Rejected quantity updates redirect silently with no user-facing error message
- `loaddata products` will overwrite admin edits because the fixture still stores Chicken Wings at 11.49 (pk 2) and Chocolate Milkshake at 5.49 (pk 5)
- Fixture image URLs depend on Unsplash remaining reachable
- Default development `SECRET_KEY` is committed in `settings.py`; `DEBUG = True`; `ALLOWED_HOSTS = []` (fine for class use; not production-ready)
- Non-dict `session['cart']` values are treated as empty for the request but are not automatically repaired in the session until a mutating view writes a new dict
- The menu query has no `order_by`
- Intentionally postponed: checkout, orders, payment, delivery, pickup details, customer accounts, APIs, React, a custom owner dashboard

### 7. Current Development Stage

The catalog stage is complete.

The session shopping cart stage is **complete**: add, view, totals, empty state, customer navigation, increase, decrease, absolute update, remove, server-side 1..20 quantity limit, and progressive-enhancement JS for quantity controls.

No new product stage has been started. Do not begin checkout or orders unless explicitly requested.

### 8. Next Planned Step

Fix the deleted-product / orphan session-key mismatch: when a product id in `request.session['cart']` has no matching `Product`, remove that key (or otherwise ensure `cart_count` matches only displayable lines) so the nav badge cannot over-count relative to `/cart/`. Keep the change small. Do not add checkout, `Order`, `OrderItem`, pickup information, payment, or customer accounts. Do not run `loaddata products`.

### 9. Files Most Relevant to the Next Step

- `docs/PROJECT_CONTEXT.md`
- `menu/views.py`
- `menu/context_processors.py`
- `menu/tests.py`
- `menu/templates/cart.html`
- `menu/templates/nav.html`

---

*Last updated: 2026-10-06 — catalog and session shopping cart stages are complete (add/view/quantity change/remove/1–20 limit/progressive JS). Next: clean orphan session cart keys so `cart_count` matches the cart page.*
