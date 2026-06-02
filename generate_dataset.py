import json
import random

# ==================== DATASET.JSON (200 фрагментов) ====================

categories = ["auth", "database", "http", "file_io", "validation", 
              "logging", "caching", "encryption", "error_handling", "api"]

dataset = []

# ========== AUTH (20 примеров) ==========
auth_examples = [
    # Python (10)
    ("python", "def validate_jwt_token(token, secret_key):\n    try:\n        decoded = jwt.decode(token, secret_key, algorithms=['HS256'])\n        return decoded\n    except jwt.ExpiredSignatureError:\n        raise Exception('Token expired')\n    except jwt.InvalidTokenError:\n        raise Exception('Invalid token')", 
         "Проверка и декодирование JWT токена с обработкой истечения срока", "auth"),
    
    ("python", "def hash_password(password, salt=None):\n    if salt is None:\n        salt = bcrypt.gensalt()\n    hashed = bcrypt.hashpw(password.encode(), salt)\n    return hashed, salt",
         "Хеширование пароля с использованием bcrypt и соли", "auth"),
    
    ("python", "def check_password_strength(password):\n    if len(password) < 8:\n        return False\n    if not re.search(r'[A-Z]', password):\n        return False\n    if not re.search(r'[0-9]', password):\n        return False\n    return True",
         "Проверка сложности пароля на соответствие требованиям безопасности", "auth"),
    
    ("python", "def generate_oauth_state():\n    state = secrets.token_urlsafe(32)\n    redis_client.setex(f'oauth_state:{state}', 600, 'pending')\n    return state",
         "Генерация безопасного state параметра для OAuth flow", "auth"),
    
    ("python", "def refresh_access_token(refresh_token):\n    user = User.query.filter_by(refresh_token=refresh_token).first()\n    if not user:\n        raise Exception('Invalid refresh token')\n    new_access = create_access_token(user.id)\n    return new_access",
         "Обновление access token с использованием refresh token", "auth"),
    
    ("python", "def logout_user(user_id, token):\n    redis_client.setex(f'blacklist:{token}', 3600, 'true')\n    user = User.query.get(user_id)\n    user.last_logout = datetime.utcnow()\n    db.session.commit()",
         "Выход пользователя с добавлением токена в blacklist", "auth"),
    
    ("python", "def two_factor_auth_verify(user_id, code):\n    user = User.query.get(user_id)\n    totp = pyotp.TOTP(user.totp_secret)\n    if totp.verify(code):\n        return True\n    return False",
         "Проверка кода двухфакторной аутентификации TOTP", "auth"),
    
    ("python", "def create_session(user_id, ip_address):\n    session = Session(user_id=user_id, ip=ip_address, created_at=datetime.utcnow())\n    session.token = secrets.token_hex(32)\n    db.session.add(session)\n    db.session.commit()\n    return session.token",
         "Создание новой пользовательской сессии с токеном", "auth"),
    
    ("python", "def verify_api_key(api_key):\n    key = APIKey.query.filter_by(key=api_key, active=True).first()\n    if not key:\n        return None\n    if key.expires_at < datetime.utcnow():\n        return None\n    return key.user",
         "Проверка валидности API ключа и его срока действия", "auth"),
    
    ("python", "def reset_password_request(email):\n    user = User.query.filter_by(email=email).first()\n    if user:\n        token = user.get_reset_password_token()\n        send_password_reset_email(user.email, token)",
         "Запрос сброса пароля с отправкой email с токеном", "auth"),
    
    # Java (10)
    ("java", "public boolean authenticateUser(String username, String password) {\n    User user = userRepository.findByUsername(username);\n    if (user == null) return false;\n    return passwordEncoder.matches(password, user.getPasswordHash());\n}",
         "Аутентификация пользователя по логину и паролю", "auth"),
    
    ("java", "public String generateJwtToken(UserDetails userDetails) {\n    return Jwts.builder()\n        .setSubject(userDetails.getUsername())\n        .setIssuedAt(new Date())\n        .setExpiration(new Date(System.currentTimeMillis() + 3600000))\n        .signWith(SignatureAlgorithm.HS256, secretKey)\n        .compact();\n}",
         "Генерация JWT токена с временем истечения", "auth"),
    
    ("java", "public void invalidateSession(String sessionId) {\n    Session session = sessionRepository.findById(sessionId);\n    if (session != null) {\n        session.setActive(false);\n        session.setInvalidatedAt(new Date());\n        sessionRepository.save(session);\n    }\n}",
         "Деактивация пользовательской сессии", "auth"),
    
    ("java", "public boolean hasRole(User user, String roleName) {\n    return user.getRoles().stream()\n        .anyMatch(role -> role.getName().equals(roleName));\n}",
         "Проверка наличия у пользователя определенной роли", "auth"),
    
    ("java", "public void lockAccount(String username) {\n    User user = userRepository.findByUsername(username);\n    user.setAccountLocked(true);\n    user.setLockTime(new Date());\n    userRepository.save(user);\n}",
         "Блокировка учетной записи пользователя", "auth"),
    
    ("java", "public String encryptPassword(String password) {\n    MessageDigest md = MessageDigest.getInstance(\"SHA-256\");\n    byte[] hash = md.digest(password.getBytes(StandardCharsets.UTF_8));\n    return Base64.getEncoder().encodeToString(hash);\n}",
         "Шифрование пароля с использованием SHA-256", "auth"),
    
    ("java", "public boolean validateSession(String token) {\n    Session session = sessionRepository.findByToken(token);\n    return session != null && session.isActive() \n        && session.getExpiresAt().after(new Date());\n}",
         "Проверка валидности сессионного токена", "auth"),
    
    ("java", "public void updateLastLogin(String userId) {\n    User user = userRepository.findById(userId);\n    user.setLastLoginDate(new Date());\n    userRepository.save(user);\n}",
         "Обновление времени последнего входа пользователя", "auth"),
    
    ("java", "public boolean checkPasswordHistory(String userId, String newPassword) {\n    List<String> oldPasswords = passwordHistoryRepository.findLast5Passwords(userId);\n    return oldPasswords.stream().noneMatch(p -> passwordEncoder.matches(newPassword, p));\n}",
         "Проверка что новый пароль не использовался ранее", "auth"),
    
    ("java", "public void registerFailedLogin(String username) {\n    int attempts = failedLoginCache.incrementAndGet(username);\n    if (attempts >= 5) {\n        lockAccount(username);\n    }\n}",
         "Регистрация неудачной попытки входа и блокировка после 5 попыток", "auth"),
]

for lang, code, desc, cat in auth_examples:
    dataset.append({"id": len(dataset)+1, "language": lang, "code": code, "description": desc, "category": cat})

# ========== DATABASE (20 примеров) ==========
db_examples = [
    # Python (10)
    ("python", "def get_user_by_id(user_id):\n    return db.session.query(User).filter(User.id == user_id).first()",
     "Получение пользователя из базы данных по идентификатору", "database"),
    
    ("python", "def create_database_connection(host, port, database, user, password):\n    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')\n    return engine.connect()",
     "Установка соединения с PostgreSQL базой данных", "database"),
    
    ("python", "def bulk_insert_users(users_list):\n    db.session.bulk_insert_mappings(User, users_list)\n    db.session.commit()",
     "Массовая вставка записей пользователей в базу данных", "database"),
    
    ("python", "def update_user_email(user_id, new_email):\n    user = User.query.get(user_id)\n    user.email = new_email\n    db.session.commit()\n    return user",
     "Обновление email пользователя в базе данных", "database"),
    
    ("python", "def delete_soft_record(model, record_id):\n    record = model.query.get(record_id)\n    record.deleted_at = datetime.utcnow()\n    db.session.commit()",
     "Мягкое удаление записи с установкой timestamp", "database"),
    
    ("python", "def get_paginated_results(query, page, per_page):\n    return query.paginate(page=page, per_page=per_page, error_out=False)",
     "Пагинация результатов запроса к базе данных", "database"),
    
    ("python", "def execute_raw_query(query, params):\n    result = db.session.execute(query, params)\n    return result.fetchall()",
     "Выполнение сырого SQL запроса с параметрами", "database"),
    
    ("python", "def create_transaction():\n    try:\n        db.session.begin()\n        yield db.session\n        db.session.commit()\n    except:\n        db.session.rollback()\n        raise",
     "Управление транзакцией базы данных с commit/rollback", "database"),
    
    ("python", "def get_db_stats():\n    total_users = User.query.count()\n    active_sessions = Session.query.filter_by(active=True).count()\n    return {'users': total_users, 'sessions': active_sessions}",
     "Получение статистики базы данных", "database"),
    
    ("python", "def migrate_database():\n    from alembic import command\n    from alembic.config import Config\n    alembic_cfg = Config(\"alembic.ini\")\n    command.upgrade(alembic_cfg, \"head\")",
     "Применение миграций базы данных через Alembic", "database"),
    
    # Java (10)
    ("java", "public User findById(Long id) {\n    return entityManager.find(User.class, id);\n}",
     "Поиск сущности по первичному ключу", "database"),
    
    ("java", "public List<User> findByEmail(String email) {\n    return entityManager.createQuery(\"SELECT u FROM User u WHERE u.email = :email\", User.class)\n        .setParameter(\"email\", email)\n        .getResultList();\n}",
     "Поиск пользователей по email через JPQL запрос", "database"),
    
    ("java", "public void saveUser(User user) {\n    if (user.getId() == null) {\n        entityManager.persist(user);\n    } else {\n        entityManager.merge(user);\n    }\n}",
     "Сохранение пользователя (insert или update)", "database"),
    
    ("java", "public void deleteUser(Long id) {\n    User user = findById(id);\n    if (user != null) {\n        entityManager.remove(user);\n    }\n}",
     "Удаление сущности из базы данных", "database"),
    
    ("java", "public Page<User> findUsersPaginated(int page, int size) {\n    return userRepository.findAll(PageRequest.of(page, size));\n}",
     "Пагинированный список пользователей через Spring Data", "database"),
    
    ("java", "public long countActiveUsers() {\n    return userRepository.countByActiveTrue();\n}",
     "Подсчет активных пользователей", "database"),
    
    ("java", "public void batchInsert(List<User> users) {\n    int count = 0;\n    for (User user : users) {\n        entityManager.persist(user);\n        if (++count % 50 == 0) {\n            entityManager.flush();\n            entityManager.clear();\n        }\n    }\n}",
     "Пакетная вставка записей с периодическим flush", "database"),
    
    ("java", "public Optional<User> findByUsername(String username) {\n    return userRepository.findByUsername(username);\n}",
     "Поиск пользователя по имени пользователя", "database"),
    
    ("java", "public void updatePassword(Long userId, String newPassword) {\n    User user = findById(userId);\n    user.setPasswordHash(passwordEncoder.encode(newPassword));\n    entityManager.merge(user);\n}",
     "Обновление хеша пароля пользователя", "database"),
    
    ("java", "public List<User> searchUsers(String searchTerm) {\n    return entityManager.createQuery(\n        \"SELECT u FROM User u WHERE u.username LIKE :term OR u.email LIKE :term\", User.class)\n        .setParameter(\"term\", \"%\" + searchTerm + \"%\")\n        .getResultList();\n}",
     "Поиск пользователей по частичному совпадению имени или email", "database"),
]

for lang, code, desc, cat in db_examples:
    dataset.append({"id": len(dataset)+1, "language": lang, "code": code, "description": desc, "category": cat})

# ========== HTTP (20 примеров) ==========
http_examples = [
    # Python (10)
    ("python", "def make_get_request(url, headers=None):\n    response = requests.get(url, headers=headers, timeout=30)\n    response.raise_for_status()\n    return response.json()",
     "Выполнение GET запроса с обработкой ошибок и таймаутом", "http"),
    
    ("python", "def post_json_data(url, data, api_key):\n    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}\n    response = requests.post(url, json=data, headers=headers)\n    return response.status_code, response.json()",
     "Отправка POST запроса с JSON данными и авторизацией", "http"),
    
    ("python", "def download_file(url, save_path):\n    response = requests.get(url, stream=True)\n    with open(save_path, 'wb') as f:\n        for chunk in response.iter_content(chunk_size=8192):\n            f.write(chunk)",
     "Скачивание файла по URL с потоковой записью", "http"),
    
    ("python", "def upload_file(url, file_path):\n    with open(file_path, 'rb') as f:\n        files = {'file': f}\n        response = requests.post(url, files=files)\n    return response.json()",
     "Загрузка файла на сервер через multipart form", "http"),
    
    ("python", "def make_retry_request(url, max_retries=3):\n    for attempt in range(max_retries):\n        try:\n            response = requests.get(url, timeout=10)\n            return response\n        except requests.RequestException:\n            if attempt == max_retries - 1:\n                raise\n            time.sleep(2 ** attempt)",
     "HTTP запрос с экспоненциальной задержкой при retry", "http"),
    
    ("python", "def set_session_cookies(session, username, password):\n    session.post('https://api.example.com/login', json={'user': username, 'pass': password})\n    return session",
     "Создание сессии с cookies после аутентификации", "http"),
    
    ("python", "def handle_http_errors(response):\n    if response.status_code == 404:\n        raise ResourceNotFoundError()\n    elif response.status_code == 401:\n        raise AuthenticationError()\n    elif response.status_code >= 500:\n        raise ServerError()",
     "Обработка HTTP ошибок по кодам статуса", "http"),
    
    ("python", "def add_rate_limiting(headers):\n    headers['X-RateLimit-Limit'] = '1000'\n    headers['X-RateLimit-Remaining'] = '999'\n    return headers",
     "Добавление заголовков rate limiting к ответу", "http"),
    
    ("python", "def parse_link_header(link_header):\n    links = {}\n    for part in link_header.split(','):\n        url, rel = part.split(';')\n        links[rel.split('=')[1].strip('\"')] = url.strip('<>')\n    return links",
     "Парсинг Link заголовка для пагинации", "http"),
    
    ("python", "def create_webhook_signature(payload, secret):\n    hmac_hash = hmac.new(secret.encode(), payload, hashlib.sha256)\n    return f'sha256={hmac_hash.hexdigest()}'",
     "Создание HMAC подписи для проверки webhook", "http"),
    
    # Java (10)
    ("java", "public HttpResponse sendGetRequest(String url) throws IOException {\n    HttpClient client = HttpClient.newHttpClient();\n    HttpRequest request = HttpRequest.newBuilder()\n        .uri(URI.create(url))\n        .GET()\n        .build();\n    return client.send(request, HttpResponse.BodyHandlers.ofString());\n}",
     "Отправка GET запроса через Java HttpClient", "http"),
    
    ("java", "public String postJson(String url, String jsonBody) throws IOException {\n    HttpRequest request = HttpRequest.newBuilder()\n        .uri(URI.create(url))\n        .header(\"Content-Type\", \"application/json\")\n        .POST(HttpRequest.BodyPublishers.ofString(jsonBody))\n        .build();\n    return httpClient.send(request, HttpResponse.BodyHandlers.ofString()).body();\n}",
     "POST запрос с JSON телом", "http"),
    
    ("java", "public void downloadFile(String url, Path destination) throws IOException {\n    HttpRequest request = HttpRequest.newBuilder().uri(URI.create(url)).GET().build();\n    httpClient.send(request, HttpResponse.BodyHandlers.ofFile(destination));\n}",
     "Скачивание файла по URL в указанный путь", "http"),
    
    ("java", "public HttpResponse sendWithTimeout(String url, int timeoutSeconds) {\n    HttpRequest request = HttpRequest.newBuilder()\n        .uri(URI.create(url))\n        .timeout(Duration.ofSeconds(timeoutSeconds))\n        .GET()\n        .build();\n    return httpClient.send(request, HttpResponse.BodyHandlers.ofString());\n}",
     "HTTP запрос с таймаутом", "http"),
    
    ("java", "public void addAuthHeader(HttpRequest.Builder builder, String token) {\n    builder.header(\"Authorization\", \"Bearer \" + token);\n}",
     "Добавление Bearer токена в заголовок запроса", "http"),
    
    ("java", "public boolean checkResponseStatus(HttpResponse response, int expectedCode) {\n    return response.statusCode() == expectedCode;\n}",
     "Проверка кода статуса HTTP ответа", "http"),
    
    ("java", "public Map<String, String> parseCookies(String cookieHeader) {\n    Map<String, String> cookies = new HashMap<>();\n    for (String cookie : cookieHeader.split(\";\")) {\n        String[] parts = cookie.trim().split(\"=\");\n        cookies.put(parts[0], parts[1]);\n    }\n    return cookies;\n}",
     "Парсинг Cookie заголовка в Map", "http"),
    
    ("java", "public void setRateLimitHeaders(HttpResponse response) {\n    response.headers().firstValue(\"X-RateLimit-Remaining\").ifPresent(System.out::println);\n}",
     "Чтение заголовков rate limiting из ответа", "http"),
    
    ("java", "public HttpResponse retryRequest(String url, int maxRetries) throws IOException {\n    for (int i = 0; i < maxRetries; i++) {\n        try {\n            return sendGetRequest(url);\n        } catch (IOException e) {\n            if (i == maxRetries - 1) throw e;\n            Thread.sleep(1000 * (i + 1));\n        }\n    }\n}",
     "Повтор запроса с задержкой при ошибке", "http"),
    
    ("java", "public String buildQueryString(Map<String, String> params) {\n    return params.entrySet().stream()\n        .map(e -> e.getKey() + \"=\" + URLEncoder.encode(e.getValue(), StandardCharsets.UTF_8))\n        .collect(Collectors.joining(\"&\"));\n}",
     "Построение query string из параметров", "http"),
]

for lang, code, desc, cat in http_examples:
    dataset.append({"id": len(dataset)+1, "language": lang, "code": code, "description": desc, "category": cat})

# ========== FILE_IO (20 примеров) ==========
file_examples = [
    # Python (10)
    ("python", "def read_file_safely(filepath):\n    try:\n        with open(filepath, 'r', encoding='utf-8') as f:\n            return f.read()\n    except FileNotFoundError:\n        return None",
     "Безопасное чтение файла с обработкой отсутствия", "file_io"),
    
    ("python", "def write_json_to_file(data, filepath):\n    with open(filepath, 'w', encoding='utf-8') as f:\n        json.dump(data, f, indent=2, ensure_ascii=False)",
     "Запись данных в JSON файл с форматированием", "file_io"),
    
    ("python", "def read_csv_file(filepath):\n    with open(filepath, 'r', encoding='utf-8') as f:\n        reader = csv.DictReader(f)\n        return list(reader)",
     "Чтение CSV файла в список словарей", "file_io"),
    
    ("python", "def append_to_log(filepath, message):\n    with open(filepath, 'a', encoding='utf-8') as f:\n        timestamp = datetime.now().isoformat()\n        f.write(f'[{timestamp}] {message}\\n')",
     "Добавление записи в лог файл с timestamp", "file_io"),
    
    ("python", "def get_file_size(filepath):\n    return os.path.getsize(filepath)",
     "Получение размера файла в байтах", "file_io"),
    
    ("python", "def list_files_in_directory(directory, extension=None):\n    files = os.listdir(directory)\n    if extension:\n        files = [f for f in files if f.endswith(extension)]\n    return files",
     "Список файлов в директории с фильтрацией по расширению", "file_io"),
    
    ("python", "def copy_file(source, destination):\n    shutil.copy2(source, destination)",
     "Копирование файла с сохранением метаданных", "file_io"),
    
    ("python", "def read_large_file_chunked(filepath, chunk_size=8192):\n    with open(filepath, 'rb') as f:\n        while chunk := f.read(chunk_size):\n            yield chunk",
     "Чтение большого файла частями (generator)", "file_io"),
    
    ("python", "def create_directory_if_not_exists(path):\n    os.makedirs(path, exist_ok=True)",
     "Создание директории если она не существует", "file_io"),
    
    ("python", "def delete_file(filepath):\n    if os.path.exists(filepath):\n        os.remove(filepath)",
     "Удаление файла если он существует", "file_io"),
    
    # Java (10)
    ("java", "public String readFileToString(Path path) throws IOException {\n    return Files.readString(path, StandardCharsets.UTF_8);\n}",
     "Чтение файла в строку", "file_io"),
    
    ("java", "public void writeStringToFile(Path path, String content) throws IOException {\n    Files.writeString(path, content, StandardCharsets.UTF_8, StandardOpenOption.CREATE);\n}",
     "Запись строки в файл", "file_io"),
    
    ("java", "public List<String> readAllLines(Path path) throws IOException {\n    return Files.readAllLines(path, StandardCharsets.UTF_8);\n}",
     "Чтение всех строк файла в список", "file_io"),
    
    ("java", "public void copyFile(Path source, Path target) throws IOException {\n    Files.copy(source, target, StandardCopyOption.REPLACE_EXISTING);\n}",
     "Копирование файла с заменой существующего", "file_io"),
    
    ("java", "public boolean deleteFile(Path path) {\n    try {\n        return Files.deleteIfExists(path);\n    } catch (IOException e) {\n        return false;\n    }\n}",
     "Удаление файла с проверкой существования", "file_io"),
    
    ("java", "public long getFileSize(Path path) {\n    try {\n        return Files.size(path);\n    } catch (IOException e) {\n        return -1;\n    }\n}",
     "Получение размера файла", "file_io"),
    
    ("java", "public Stream<Path> listFiles(Path directory) throws IOException {\n    return Files.list(directory);\n}",
     "Список файлов в директории как Stream", "file_io"),
    
    ("java", "public void createDirectories(Path path) throws IOException {\n    Files.createDirectories(path);\n}",
     "Создание директории и всех родительских", "file_io"),
    
    ("java", "public boolean fileExists(Path path) {\n    return Files.exists(path);\n}",
     "Проверка существования файла", "file_io"),
    
    ("java", "public void moveFile(Path source, Path target) throws IOException {\n    Files.move(source, target, StandardCopyOption.REPLACE_EXISTING);\n}",
     "Перемещение файла в другую директорию", "file_io"),
]

for lang, code, desc, cat in file_examples:
    dataset.append({"id": len(dataset)+1, "language": lang, "code": code, "description": desc, "category": cat})

# ========== VALIDATION (20 примеров) ==========
validation_examples = [
    # Python (10)
    ("python", "def validate_email(email):\n    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'\n    return re.match(pattern, email) is not None",
     "Валидация email адреса через regex", "validation"),
    
    ("python", "def validate_phone_number(phone):\n    digits = re.sub(r'\\D', '', phone)\n    return len(digits) == 11 and digits[0] == '7'",
     "Проверка валидности российского номера телефона", "validation"),
    
    ("python", "def validate_date_format(date_string):\n    try:\n        datetime.strptime(date_string, '%Y-%m-%d')\n        return True\n    except ValueError:\n        return False",
     "Проверка формата даты YYYY-MM-DD", "validation"),
    
    ("python", "def validate_json_schema(data, schema):\n    try:\n        jsonschema.validate(data, schema)\n        return True\n    except jsonschema.ValidationError:\n        return False",
     "Валидация JSON данных по JSON Schema", "validation"),
    
    ("python", "def validate_credit_card(number):\n    def luhn_check(card_number):\n        digits = [int(d) for d in str(card_number)]\n        checksum = sum(digits[::-2] + [sum(divmod(d*2, 10)) for d in digits[-2::-2]])\n        return checksum % 10 == 0\n    return luhn_check(number)",
     "Проверка номера кредитной карты алгоритмом Луна", "validation"),
    
    ("python", "def validate_username(username):\n    if len(username) < 3 or len(username) > 20:\n        return False\n    return re.match(r'^[a-zA-Z0-9_]+$', username) is not None",
     "Валидация имени пользователя по длине и символам", "validation"),
    
    ("python", "def validate_file_extension(filename, allowed_extensions):\n    ext = os.path.splitext(filename)[1].lower()\n    return ext in allowed_extensions",
     "Проверка расширения файла на разрешенные", "validation"),
    
    ("python", "def validate_ip_address(ip):\n    try:\n        ipaddress.ip_address(ip)\n        return True\n    except ValueError:\n        return False",
     "Проверка валидности IP адреса", "validation"),
    
    ("python", "def validate_required_fields(data, required_fields):\n    return all(field in data and data[field] for field in required_fields)",
     "Проверка наличия всех обязательных полей", "validation"),
    
    ("python", "def validate_password_match(password, confirm_password):\n    return password == confirm_password",
     "Проверка совпадения пароля и подтверждения", "validation"),
    
    # Java (10)
    ("java", "public boolean isValidEmail(String email) {\n    String regex = \"^[A-Za-z0-9+_.-]+@(.+)$\";\n    return Pattern.matches(regex, email);\n}",
     "Валидация email через регулярное выражение", "validation"),
    
    ("java", "public boolean isNotNullOrEmpty(String str) {\n    return str != null && !str.trim().isEmpty();\n}",
     "Проверка что строка не null и не пустая", "validation"),
    
    ("java", "public boolean isValidAge(int age) {\n    return age >= 18 && age <= 120;\n}",
     "Проверка что возраст в допустимом диапазоне", "validation"),
    
    ("java", "public boolean isValidUrl(String url) {\n    try {\n        new URL(url).toURI();\n        return true;\n    } catch (Exception e) {\n        return false;\n    }\n}",
     "Проверка валидности URL", "validation"),
    
    ("java", "public boolean containsOnlyDigits(String str) {\n    return str != null && str.matches(\"\\\\d+\");\n}",
     "Проверка что строка содержит только цифры", "validation"),
    
    ("java", "public boolean isValidDate(LocalDate date) {\n    return date != null && date.isAfter(LocalDate.of(1900, 1, 1));\n}",
     "Проверка что дата не null и после 1900 года", "validation"),
    
    ("java", "public boolean isValidLength(String str, int min, int max) {\n    return str != null && str.length() >= min && str.length() <= max;\n}",
     "Проверка длины строки в диапазоне", "validation"),
    
    ("java", "public boolean isPositiveNumber(BigDecimal number) {\n    return number != null && number.compareTo(BigDecimal.ZERO) > 0;\n}",
     "Проверка что число положительное", "validation"),
    
    ("java", "public boolean isValidEnum(String value, Class<? extends Enum> enumClass) {\n    try {\n        Enum.valueOf(enumClass, value);\n        return true;\n    } catch (IllegalArgumentException e) {\n        return false;\n    }\n}",
     "Проверка что строка является валидным значением enum", "validation"),
    
    ("java", "public boolean isUniqueUsername(String username, UserRepository repo) {\n    return repo.findByUsername(username) == null;\n}",
     "Проверка уникальности имени пользователя", "validation"),
]

for lang, code, desc, cat in validation_examples:
    dataset.append({"id": len(dataset)+1, "language": lang, "code": code, "description": desc, "category": cat})

# ========== LOGGING (20 примеров) ==========
logging_examples = [
    # Python (10)
    ("python", "def setup_logger(name, level=logging.INFO):\n    logger = logging.getLogger(name)\n    logger.setLevel(level)\n    handler = logging.StreamHandler()\n    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')\n    handler.setFormatter(formatter)\n    logger.addHandler(handler)\n    return logger",
     "Настройка логгера с форматированием и handler", "logging"),
    
    ("python", "def log_error_to_file(error_msg, filepath='error.log'):\n    logging.basicConfig(filename=filepath, level=logging.ERROR)\n    logging.error(error_msg, exc_info=True)",
     "Логирование ошибки в файл с traceback", "logging"),
    
    ("python", "def log_request(logger, request):\n    logger.info(f'{request.method} {request.path} - {request.remote_addr}')",
     "Логирование HTTP запроса с методом и IP", "logging"),
    
    ("python", "def log_performance(start_time, operation):\n    duration = time.time() - start_time\n    logging.info(f'{operation} completed in {duration:.2f}s')",
     "Логирование времени выполнения операции", "logging"),
    
    ("python", "def create_rotating_log(filepath, max_bytes=1048576, backup_count=5):\n    handler = RotatingFileHandler(filepath, maxBytes=max_bytes, backupCount=backup_count)\n    return handler",
     "Создание ротационного лог файла с ограничением размера", "logging"),
    
    ("python", "def log_debug_data(data):\n    logging.debug(json.dumps(data, default=str))",
     "Логирование отладочных данных в JSON формате", "logging"),
    
    ("python", "def log_user_action(user_id, action, details):\n    logging.info(f'User {user_id} performed {action}: {details}')",
     "Логирование действий пользователя с деталями", "logging"),
    
    ("python", "def setup_json_logger():\n    handler = logging.StreamHandler()\n    formatter = jsonlogger.JsonFormatter()\n    handler.setFormatter(formatter)\n    logging.getLogger().addHandler(handler)",
     "Настройка логгера в JSON формате", "logging"),
    
    ("python", "def log_with_context(logger, context_dict):\n    extra_logger = logging.LoggerAdapter(logger, context_dict)\n    return extra_logger",
     "Создание логгера с контекстной информацией", "logging"),
    
    ("python", "def silence_external_logs():\n    logging.getLogger('urllib3').setLevel(logging.WARNING)\n    logging.getLogger('requests').setLevel(logging.WARNING)",
     "Отключение verbose логов внешних библиотек", "logging"),
    
    # Java (10)
    ("java", "private static final Logger logger = LoggerFactory.getLogger(MyClass.class);\n\npublic void logInfo(String message) {\n    logger.info(message);\n}",
     "Логирование INFO уровня через SLF4J", "logging"),
    
    ("java", "public void logErrorWithException(String message, Exception e) {\n    logger.error(message, e);\n}",
     "Логирование ошибки с исключением и stack trace", "logging"),
    
    ("java", "public void logDebugData(Object data) {\n    logger.debug(\"Data: {}\", data);\n}",
     "Отладочное логирование с placeholder", "logging"),
    
    ("java", "public void setupFileLogger(String filepath) throws IOException {\n    FileHandler fileHandler = new FileHandler(filepath, true);\n    logger.addHandler(fileHandler);\n}",
     "Настройка файлового handler для логгера", "logging"),
    
    ("java", "public void logRequestMethod(HttpServletRequest request) {\n    logger.info(\"Request: {} {}\", request.getMethod(), request.getRequestURI());\n}",
     "Логирование HTTP запроса с методом и URI", "logging"),
    
    ("java", "public void logExecutionTime(String operation, long durationMs) {\n    logger.info(\"{} executed in {} ms\", operation, durationMs);\n}",
     "Логирование времени выполнения операции", "logging"),
    
    ("java", "public void logUserActivity(Long userId, String action) {\n    logger.info(\"User {} performed action: {}\", userId, action);\n}",
     "Логирование активности пользователя", "logging"),
    
    ("java", "public void setLogLevel(Level level) {\n    logger.setLevel(level);\n}",
     "Установка уровня логирования", "logging"),
    
    ("java", "public void logWithMdc(String requestId) {\n    MDC.put(\"requestId\", requestId);\n    logger.info(\"Processing request\");\n    MDC.clear();\n}",
     "Логирование с MDC контекстом (requestId)", "logging"),
    
    ("java", "public void logWarning(String message, Object... args) {\n    logger.warn(message, args);\n}",
     "Логирование WARNING уровня с параметрами", "logging"),
]

for lang, code, desc, cat in logging_examples:
    dataset.append({"id": len(dataset)+1, "language": lang, "code": code, "description": desc, "category": cat})

# ========== CACHING (20 примеров) ==========
caching_examples = [
    # Python (10)
    ("python", "def get_from_cache(key):\n    return redis_client.get(key)",
     "Получение значения из Redis cache по ключу", "caching"),
    
    ("python", "def set_cache(key, value, ttl=3600):\n    redis_client.setex(key, ttl, json.dumps(value))",
     "Установка значения в cache с временем жизни", "caching"),
    
    ("python", "@lru_cache(maxsize=128)\ndef expensive_computation(n):\n    return sum(i**2 for i in range(n))",
     "Кэширование функции через LRU decorator", "caching"),
    
    ("python", "def invalidate_cache(pattern):\n    keys = redis_client.keys(pattern)\n    if keys:\n        redis_client.delete(*keys)",
     "Инвалидация кэша по паттерну ключей", "caching"),
    
    ("python", "def get_or_set_cache(key, fetch_func, ttl=300):\n    cached = redis_client.get(key)\n    if cached:\n        return json.loads(cached)\n    data = fetch_func()\n    redis_client.setex(key, ttl, json.dumps(data))\n    return data",
     "Получение из кэша или вычисление и сохранение", "caching"),
    
    ("python", "def cache_page(view_func):\n    @wraps(view_func)\n    def wrapper(request):\n        cache_key = f'page:{request.path}'\n        cached = cache.get(cache_key)\n        if cached:\n            return cached\n        response = view_func(request)\n        cache.set(cache_key, response, 300)\n        return response\n    return wrapper",
     "Декоратор для кэширования страниц", "caching"),
    
    ("python", "def warm_up_cache():\n    popular_items = db.query(PopularItem).all()\n    for item in popular_items:\n        cache.set(f'item:{item.id}', item.to_dict(), 3600)",
     "Предварительное заполнение кэша популярными данными", "caching"),
    
    ("python", "def get_cache_stats():\n    info = redis_client.info('stats')\n    return {'hits': info['keyspace_hits'], 'misses': info['keyspace_misses']}",
     "Получение статистики hit/miss кэша", "caching"),
    
    ("python", "def set_nested_cache(keys, value):\n    key = ':'.join(str(k) for k in keys)\n    redis_client.setex(key, 600, json.dumps(value))",
     "Кэширование с составным ключом", "caching"),
    
    ("python", "def clear_all_cache():\n    redis_client.flushdb()",
     "Очистка всего кэша базы данных", "caching"),
    
    # Java (10)
    ("java", "@Cacheable(value = \"users\", key = \"#id\")\npublic User getUserById(Long id) {\n    return userRepository.findById(id);\n}",
     "Кэширование метода через Spring Cache annotation", "caching"),
    
    ("java", "public void putInCache(String key, Object value) {\n    cache.put(key, value);\n}",
     "Помещение объекта в кэш", "caching"),
    
    ("java", "public Object getFromCache(String key) {\n    return cache.get(key);\n}",
     "Получение объекта из кэша по ключу", "caching"),
    
    ("java", "@CacheEvict(value = \"users\", key = \"#id\")\npublic void deleteUser(Long id) {\n    userRepository.deleteById(id);\n}",
     "Удаление из кэша при удалении сущности", "caching"),
    
    ("java", "public void clearCache(String cacheName) {\n    cacheManager.getCache(cacheName).clear();\n}",
     "Очистка всего кэша по имени", "caching"),
    
    ("java", "@CachePut(value = \"users\", key = \"#user.id\")\npublic User updateUser(User user) {\n    return userRepository.save(user);\n}",
     "Обновление кэша при изменении данных", "caching"),
    
    ("java", "public Cache getCache(String name) {\n    return cacheManager.getCache(name);\n}",
     "Получение экземпляра кэша по имени", "caching"),
    
    ("java", "public void setCacheTtl(String key, long ttl, TimeUnit unit) {\n    cache.put(key, value, ttl, unit);\n}",
     "Установка времени жизни для записи в кэше", "caching"),
    
    ("java", "public boolean isInCache(String key) {\n    return cache.get(key) != null;\n}",
     "Проверка наличия ключа в кэше", "caching"),
    
    ("java", "public void warmUpCache() {\n    List<User> users = userRepository.findAll();\n    users.forEach(u -> cache.put(\"user:\" + u.getId(), u));\n}",
     "Предварительная загрузка данных в кэш", "caching"),
]

for lang, code, desc, cat in caching_examples:
    dataset.append({"id": len(dataset)+1, "language": lang, "code": code, "description": desc, "category": cat})

# ========== ENCRYPTION (20 примеров) ==========
encryption_examples = [
    # Python (10)
    ("python", "def encrypt_aes(data, key):\n    cipher = AES.new(key, AES.MODE_GCM)\n    ciphertext, tag = cipher.encrypt_and_digest(data.encode())\n    return cipher.nonce, ciphertext, tag",
     "Шифрование данных через AES-GCM", "encryption"),
    
    ("python", "def decrypt_aes(nonce, ciphertext, tag, key):\n    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)\n    plaintext = cipher.decrypt_and_verify(ciphertext, tag)\n    return plaintext.decode()",
     "Расшифровка AES-GCM с проверкой тега", "encryption"),
    
    ("python", "def generate_rsa_keys():\n    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)\n    public_key = private_key.public_key()\n    return private_key, public_key",
     "Генерация пары RSA ключей", "encryption"),
    
    ("python", "def hash_sha256(data):\n    return hashlib.sha256(data.encode()).hexdigest()",
     "Вычисление SHA-256 хеша строки", "encryption"),
    
    ("python", "def encrypt_rsa(message, public_key):\n    ciphertext = public_key.encrypt(message.encode(), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256())))\n    return ciphertext",
     "Шифрование RSA с OAEP padding", "encryption"),
    
    ("python", "def create_hmac(message, secret):\n    return hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()",
     "Создание HMAC подписи сообщения", "encryption"),
    
    ("python", "def derive_key(password, salt):\n    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)",
     "Получение ключа из пароля через PBKDF2", "encryption"),
    
    ("python", "def generate_random_key(length=32):\n    return secrets.token_bytes(length)",
     "Генерация криптографически случайного ключа", "encryption"),
    
    ("python", "def sign_message(private_key, message):\n    signature = private_key.sign(message.encode(), padding.PSS(mgf=padding.MGF1(hashes.SHA256())), hashes.SHA256())\n    return signature",
     "Подпись сообщения приватным RSA ключом", "encryption"),
    
    ("python", "def verify_signature(public_key, message, signature):\n    public_key.verify(signature, message.encode(), padding.PSS(mgf=padding.MGF1(hashes.SHA256())), hashes.SHA256())\n    return True",
     "Проверка цифровой подписи", "encryption"),
    
    # Java (10)
    ("java", "public String encryptAES(String data, String key) throws Exception {\n    Cipher cipher = Cipher.getInstance(\"AES/GCM/NoPadding\");\n    SecretKeySpec keySpec = new SecretKeySpec(key.getBytes(), \"AES\");\n    cipher.init(Cipher.ENCRYPT_MODE, keySpec);\n    return Base64.getEncoder().encodeToString(cipher.doFinal(data.getBytes()));\n}",
     "AES шифрование в Java", "encryption"),
    
    ("java", "public String hashSHA256(String input) throws NoSuchAlgorithmException {\n    MessageDigest md = MessageDigest.getInstance(\"SHA-256\");\n    byte[] hash = md.digest(input.getBytes(StandardCharsets.UTF_8));\n    return String.format(\"%064x\", new BigInteger(1, hash));\n}",
     "Вычисление SHA-256 хеша", "encryption"),
    
    ("java", "public KeyPair generateRSAKeyPair() throws NoSuchAlgorithmException {\n    KeyPairGenerator keyGen = KeyPairGenerator.getInstance(\"RSA\");\n    keyGen.initialize(2048);\n    return keyGen.generateKeyPair();\n}",
     "Генерация RSA ключей", "encryption"),
    
    ("java", "public String createHMAC(String message, String secret) throws Exception {\n    Mac mac = Mac.getInstance(\"HmacSHA256\");\n    mac.init(new SecretKeySpec(secret.getBytes(), \"HmacSHA256\"));\n    return Base64.getEncoder().encodeToString(mac.doFinal(message.getBytes()));\n}",
     "Создание HMAC SHA-256", "encryption"),
    
    ("java", "public byte[] encryptRSA(byte[] data, PublicKey key) throws Exception {\n    Cipher cipher = Cipher.getInstance(\"RSA/ECB/OAEPWithSHA-256AndMGF1Padding\");\n    cipher.init(Cipher.ENCRYPT_MODE, key);\n    return cipher.doFinal(data);\n}",
     "RSA шифрование с OAEP", "encryption"),
    
    ("java", "public String generateSecurePassword(int length) {\n    SecureRandom random = new SecureRandom();\n    return new BigInteger(length * 5, random).toString(32);\n}",
     "Генерация безопасного пароля", "encryption"),
    
    ("java", "public boolean verifyHMAC(String message, String signature, String secret) throws Exception {\n    String expected = createHMAC(message, secret);\n    return MessageDigest.isEqual(expected.getBytes(), signature.getBytes());\n}",
     "Проверка HMAC подписи", "encryption"),
    
    ("java", "public byte[] deriveKey(String password, byte[] salt) throws Exception {\n    PBKDF2Engine engine = new PBKDF2Engine(password, salt, 100000);\n    return engine.generateKey();\n}",
     "Получение ключа из пароля PBKDF2", "encryption"),
    
    ("java", "public Signature createSignature(PrivateKey key) throws Exception {\n    Signature signature = Signature.getInstance(\"SHA256withRSA\");\n    signature.initSign(key);\n    return signature;\n}",
     "Создание объекта подписи RSA", "encryption"),
    
    ("java", "public String encryptBase64(String data) {\n    return Base64.getEncoder().encodeToString(data.getBytes(StandardCharsets.UTF_8));\n}",
     "Base64 кодирование строки", "encryption"),
]

for lang, code, desc, cat in encryption_examples:
    dataset.append({"id": len(dataset)+1, "language": lang, "code": code, "description": desc, "category": cat})

# ========== ERROR_HANDLING (20 примеров) ==========
error_examples = [
    # Python (10)
    ("python", "def handle_division_by_zero(a, b):\n    try:\n        return a / b\n    except ZeroDivisionError:\n        return None",
     "Обработка деления на ноль", "error_handling"),
    
    ("python", "def safe_json_loads(data):\n    try:\n        return json.loads(data)\n    except json.JSONDecodeError:\n        return None",
     "Безопасный парсинг JSON с обработкой ошибок", "error_handling"),
    
    ("python", "def get_dict_value(d, key, default=None):\n    try:\n        return d[key]\n    except KeyError:\n        return default",
     "Получение значения из словаря с дефолтом", "error_handling"),
    
    ("python", "def retry_on_failure(func, max_retries=3):\n    for i in range(max_retries):\n        try:\n            return func()\n        except Exception as e:\n            if i == max_retries - 1:\n                raise\n            time.sleep(2 ** i)",
     "Повтор вызова функции при ошибке с экспоненциальной задержкой", "error_handling"),
    
    ("python", "def custom_exception_handler(func):\n    @wraps(func)\n    def wrapper(*args, **kwargs):\n        try:\n            return func(*args, **kwargs)\n        except Exception as e:\n            raise CustomAPIError(f\"Operation failed: {str(e)}\")\n    return wrapper",
     "Декоратор для обработки исключений", "error_handling"),
    
    ("python", "def validate_and_convert_int(value):\n    try:\n        return int(value)\n    except (ValueError, TypeError):\n        raise ValueError(f\"Cannot convert {value} to int\")",
     "Преобразование в int с валидацией", "error_handling"),
    
    ("python", "def handle_timeout(func, timeout_seconds):\n    try:\n        return func(timeout=timeout_seconds)\n    except TimeoutError:\n        raise ServiceUnavailableError(\"Request timed out\")",
     "Обработка таймаута операции", "error_handling"),
    
    ("python", "def suppress_exceptions(func):\n    try:\n        return func()\n    except Exception:\n        pass",
     "Подавление всех исключений", "error_handling"),
    
    ("python", "def log_and_reraise(func):\n    try:\n        return func()\n    except Exception as e:\n        logging.error(f\"Error in {func.__name__}: {e}\")\n        raise",
     "Логирование ошибки перед повторным выбросом", "error_handling"),
    
    ("python", "def handle_file_not_found(filepath):\n    try:\n        with open(filepath) as f:\n            return f.read()\n    except FileNotFoundError:\n        create_default_file(filepath)\n        return \"\"",
     "Обработка отсутствия файла созданием дефолтного", "error_handling"),
    
    # Java (10)
    ("java", "public Optional<User> findUserSafe(Long id) {\n    try {\n        return Optional.of(userRepository.findById(id));\n    } catch (EntityNotFoundException e) {\n        return Optional.empty();\n    }\n}",
     "Безопасный поиск с возвратом Optional", "error_handling"),
    
    ("java", "public int divideSafely(int a, int b) {\n    try {\n        return a / b;\n    } catch (ArithmeticException e) {\n        return 0;\n    }\n}",
     "Безопасное деление с обработкой исключения", "error_handling"),
    
    ("java", "public String parseJsonSafe(String json) {\n    try {\n        return objectMapper.readTree(json).toString();\n    } catch (JsonProcessingException e) {\n        return null;\n    }\n}",
     "Безопасный парсинг JSON", "error_handling"),
    
    ("java", "public void retryOperation(Runnable operation, int maxRetries) {\n    for (int i = 0; i < maxRetries; i++) {\n        try {\n            operation.run();\n            return;\n        } catch (Exception e) {\n            if (i == maxRetries - 1) throw e;\n        }\n    }\n}",
     "Повтор операции при ошибке", "error_handling"),
    
    ("java", "public <T> T getOrDefault(Supplier<T> supplier, T defaultValue) {\n    try {\n        return supplier.get();\n    } catch (Exception e) {\n        return defaultValue;\n    }\n}",
     "Получение значения или дефолт при ошибке", "error_handling"),
    
    ("java", "@ExceptionHandler(ResourceNotFoundException.class)\npublic ResponseEntity<ErrorResponse> handleNotFound(ResourceNotFoundException ex) {\n    return ResponseEntity.status(404).body(new ErrorResponse(ex.getMessage()));\n}",
     "Глобальный обработчик исключений REST контроллера", "error_handling"),
    
    ("java", "public void closeResourceSafely(AutoCloseable resource) {\n    try {\n        if (resource != null) resource.close();\n    } catch (Exception e) {\n        logger.error(\"Error closing resource\", e);\n    }\n}",
     "Безопасное закрытие ресурса", "error_handling"),
    
    ("java", "public Integer parseIntSafe(String value) {\n    try {\n        return Integer.parseInt(value);\n    } catch (NumberFormatException e) {\n        return null;\n    }\n}",
     "Безопасный парсинг целого числа", "error_handling"),
    
    ("java", "public void validateNotNull(Object obj, String fieldName) {\n    if (obj == null) {\n        throw new ValidationException(fieldName + \" cannot be null\");\n    }\n}",
     "Проверка на null с выбросом исключения", "error_handling"),
    
    ("java", "public CompletableFuture<String> handleTimeout(CompletableFuture<String> future, long timeout) {\n    return future.orTimeout(timeout, TimeUnit.SECONDS)\n        .exceptionally(ex -> \"Default value\");\n}",
     "Обработка таймаута CompletableFuture", "error_handling"),
]

for lang, code, desc, cat in error_examples:
    dataset.append({"id": len(dataset)+1, "language": lang, "code": code, "description": desc, "category": cat})

# ========== API (20 примеров) ==========
api_examples = [
    # Python (10)
    ("python", "@app.route('/api/users', methods=['GET'])\ndef get_users():\n    users = User.query.all()\n    return jsonify([u.to_dict() for u in users])",
     "REST API endpoint для получения списка пользователей", "api"),
    
    ("python", "@app.route('/api/users/<int:id>', methods=['POST'])\ndef create_user(id):\n    data = request.get_json()\n    user = User(id=id, **data)\n    db.session.add(user)\n    db.session.commit()\n    return jsonify(user.to_dict()), 201",
     "API endpoint создания пользователя", "api"),
    
    ("python", "def api_response(data, status=200, message='OK'):\n    return jsonify({'status': status, 'message': message, 'data': data}), status",
     "Универсальная функция ответа API", "api"),
    
    ("python", "@app.before_request\ndef check_api_key():\n    if request.endpoint and 'api' in request.endpoint:\n        api_key = request.headers.get('X-API-Key')\n        if not validate_api_key(api_key):\n            abort(401)",
     "Проверка API ключа перед запросом", "api"),
    
    ("python", "def paginate_results(query, page, per_page):\n    paginated = query.paginate(page=page, per_page=per_page)\n    return {\n        'items': [item.to_dict() for item in paginated.items],\n        'total': paginated.total,\n        'pages': paginated.pages\n    }",
     "Пагинация результатов API", "api"),
    
    ("python", "@app.route('/api/search', methods=['GET'])\ndef search():\n    query = request.args.get('q')\n    results = search_engine.search(query)\n    return jsonify({'results': results})",
     "API endpoint поиска с query параметром", "api"),
    
    ("python", "def versioned_api(route):\n    @wraps(route)\n    def wrapper(*args, **kwargs):\n        version = request.headers.get('API-Version', 'v1')\n        return route(*args, **kwargs, version=version)\n    return wrapper",
     "Декоратор для версионирования API", "api"),
    
    ("python", "@app.errorhandler(404)\ndef not_found(error):\n    return jsonify({'error': 'Not found', 'status': 404}), 404",
     "Обработчик 404 ошибки для API", "api"),
    
    ("python", "def rate_limit_decorator(max_requests=100, window=3600):\n    def decorator(f):\n        @wraps(f)\n        def wrapped(*args, **kwargs):\n            if not check_rate_limit(max_requests, window):\n                abort(429)\n            return f(*args, **kwargs)\n        return wrapped\n    return decorator",
     "Декоратор rate limiting для API endpoints", "api"),
    
    ("python", "@app.route('/api/webhook', methods=['POST'])\ndef webhook():\n    signature = request.headers.get('X-Signature')\n    payload = request.get_data()\n    if not verify_webhook_signature(payload, signature):\n        abort(401)\n    process_webhook(request.json)\n    return '', 200",
     "Webhook endpoint с проверкой подписи", "api"),
    
    # Java (10)
    ("java", "@RestController\n@RequestMapping(\"/api/users\")\npublic class UserController {\n    @GetMapping\n    public List<User> getAllUsers() {\n        return userService.findAll();\n    }\n}",
     "REST контроллер для получения пользователей", "api"),
    
    ("java", "@PostMapping(\"/api/users\")\npublic ResponseEntity<User> createUser(@RequestBody User user) {\n    User created = userService.save(user);\n    return ResponseEntity.status(201).body(created);\n}",
     "POST endpoint создания ресурса", "api"),
    
    ("java", "@GetMapping(\"/api/users/{id}\")\npublic ResponseEntity<User> getUserById(@PathVariable Long id) {\n    return userService.findById(id)\n        .map(ResponseEntity::ok)\n        .orElse(ResponseEntity.notFound().build());\n}",
     "GET endpoint получения пользователя по ID", "api"),
    
    ("java", "@PutMapping(\"/api/users/{id}\")\npublic ResponseEntity<User> updateUser(@PathVariable Long id, @RequestBody User user) {\n    user.setId(id);\n    return ResponseEntity.ok(userService.update(user));\n}",
     "PUT endpoint обновления ресурса", "api"),
    
    ("java", "@DeleteMapping(\"/api/users/{id}\")\npublic ResponseEntity<Void> deleteUser(@PathVariable Long id) {\n    userService.delete(id);\n    return ResponseEntity.noContent().build();\n}",
     "DELETE endpoint удаления ресурса", "api"),
    
    ("java", "@GetMapping(\"/api/search\")\npublic ResponseEntity<List<Result>> search(@RequestParam String q) {\n    return ResponseEntity.ok(searchService.search(q));\n}",
     "API поиска с request параметром", "api"),
    
    ("java", "@ExceptionHandler(MethodArgumentNotValidException.class)\npublic ResponseEntity<Map<String, String>> handleValidationExceptions(MethodArgumentNotValidException ex) {\n    Map<String, String> errors = new HashMap<>();\n    ex.getBindingResult().getFieldErrors().forEach(err -> errors.put(err.getField(), err.getDefaultMessage()));\n    return ResponseEntity.badRequest().body(errors);\n}",
     "Обработка ошибок валидации в API", "api"),
    
    ("java", "@GetMapping(\"/api/paginated\")\npublic Page<Item> getPaginated(@RequestParam int page, @RequestParam int size) {\n    return itemService.findAll(PageRequest.of(page, size));\n}",
     "Пагинированный API endpoint", "api"),
    
    ("java", "@CrossOrigin(origins = \"*\")\n@GetMapping(\"/api/public\")\npublic ResponseEntity<Data> getPublicData() {\n    return ResponseEntity.ok(dataService.getPublic());\n}",
     "API endpoint с CORS заголовками", "api"),
    
    ("java", "@GetMapping(value = \"/api/data\", produces = MediaType.APPLICATION_JSON_VALUE)\npublic ResponseEntity<Data> getData() {\n    return ResponseEntity.ok(dataService.getData());\n}",
     "API endpoint с указанием content type", "api"),
]

for lang, code, desc, cat in api_examples:
    dataset.append({"id": len(dataset)+1, "language": lang, "code": code, "description": desc, "category": cat})

# Сохраняем dataset
with open('dataset.json', 'w', encoding='utf-8') as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)

print(f"Создано {len(dataset)} записей")
print(f"Распределение по категориям:")
for cat in categories:
    count = len([d for d in dataset if d['category'] == cat])
    print(f"  {cat}: {count}")
print(f"Распределение по языкам:")
print(f"  Python: {len([d for d in dataset if d['language'] == 'python'])}")
print(f"  Java: {len([d for d in dataset if d['language'] == 'java'])}")

# ==================== TEST QUESTIONS (25 вопросов) ====================

test_questions = [
    "Как проверить JWT токен на валидность?",
    "Как найти пользователя в базе по ID?",
    "Как отправить POST запрос с JSON данными?",
    "Как безопасно прочитать файл?",
    "Как проверить что email корректный?",
    "Как настроить логирование в файл?",
    "Как сохранить данные в Redis кэш?",
    "Как зашифровать данные через AES?",
    "Как обработать деление на ноль?",
    "Как создать REST API endpoint?",
    "Как хешировать пароль пользователя?",
    "Как выполнить SQL запрос к базе?",
    "Как скачать файл по URL?",
    "Как создать директорию если её нет?",
    "Как проверить сложность пароля?",
    "Как логировать ошибки с traceback?",
    "Как инвалидировать кэш?",
    "Как сгенерировать RSA ключи?",
    "Как повторить запрос при ошибке?",
    "Как добавить пагинацию в API?",
    "Как проверить API ключ?",
    "Как обновить запись в базе данных?",
    "Как сделать GET запрос с таймаутом?",
    "Как записать JSON в файл?",
    "Как валидировать JSON по схеме?"
]

# Сохраняем вопросы
with open('test_questions.json', 'w', encoding='utf-8') as f:
    json.dump([{"id": i+1, "question": q} for i, q in enumerate(test_questions)], f, ensure_ascii=False, indent=2)

print(f"\nСоздано {len(test_questions)} тестовых вопросов")

# ==================== GROUND TRUTH (правильные ответы) ====================

# Сопоставляем вопросы с правильными ID из dataset
# Это примерная маппинг - нужно проверить что ID соответствуют описаниям

ground_truth = {}

# Создаем маппинг описаний на ID для удобства
desc_to_id = {}
for item in dataset:
    # Берем ключевые слова из описания
    desc_lower = item['description'].lower()
    desc_to_id[item['id']] = desc_lower

# Маппинг вопросов к правильным ID (на основе описаний)
question_to_keywords = [
    ("jwt токен", "валид", "проверк"),  # 1
    ("пользовател", "баз", "id"),  # 2
    ("post", "json", "отправ"),  # 3
    ("безопасн", "прочит", "файл"),  # 4
    ("email", "коррект", "валид"),  # 5
    ("логирован", "файл", "настро"),  # 6
    ("redis", "кэш", "сохран"),  # 7
    ("aes", "зашифр"),  # 8
    ("делен", "ноль", "обработ"),  # 9
    ("rest api", "endpoint", "созд"),  # 10
    ("хеш", "парол", "bcrypt"),  # 11
    ("sql", "запрос", "баз"),  # 12
    ("скачат", "файл", "url"),  # 13
    ("директор", "созд"),  # 14
    ("парол", "сложност", "провер"),  # 15
    ("логиров", "ошибк", "traceback"),  # 16
    ("инвалид", "кэш"),  # 17
    ("rsa", "ключ", "генер"),  # 18
    ("повтор", "ошибк", "запрос"),  # 19
    ("пагинац", "api"),  # 20
    ("api ключ", "провер"),  # 21
    ("обнов", "запис", "баз"),  # 22
    ("get", "запрос", "таймаут"),  # 23
    ("json", "файл", "запис"),  # 24
    ("json", "схем", "валид")  # 25
]

# Находим лучшие совпадения
for q_idx, (q_id, question) in enumerate([(i+1, q) for i, q in enumerate(test_questions)]):
    keywords = question_to_keywords[q_idx - 1]
    best_match = None
    best_score = -1
    
    for item in dataset:
        score = 0
        desc_lower = item['description'].lower()
        for kw in keywords:
            if kw.lower() in desc_lower:
                score += 1
        if score > best_score:
            best_score = score
            best_match = item['id']
    
    ground_truth[question] = best_match

# Сохраняем ground truth
with open('ground_truth.json', 'w', encoding='utf-8') as f:
    json.dump(ground_truth, f, ensure_ascii=False, indent=2)

print(f"Создан ground truth для {len(ground_truth)} вопросов")

print("\n✅ Датасет успешно сгенерирован!")
print("Файлы: dataset.json, test_questions.json, ground_truth.json")