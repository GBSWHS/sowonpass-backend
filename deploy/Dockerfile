FROM alpine:3.17 as builder
ARG PYTHON_VERSION=3.10

RUN apk add --update --no-cache python3 py3-pip
RUN pip install --no-cache-dir poetry

WORKDIR /app/src
COPY pyproject.toml poetry.lock /app/src/
RUN poetry config virtualenvs.create false \
    && poetry install --only main

COPY sowonpass_backend/ /app/src/sowonpass_backend/
RUN poetry build && pip install --no-cache-dir dist/*.whl
RUN rm -rf dist poetry.lock pyproject.toml sowonpass_backend

WORKDIR /usr/lib/python${PYTHON_VERSION}/site-packages
# [AUTO ADD PARAMS]
RUN find /usr/lib/python${PYTHON_VERSION}/site-packages/ -mindepth 1 -maxdepth 1 -type d ! \( -name 'uvicorn*' -o -name 'greenlet*' -o -name 'sowonpass_backend*' -o -name 'pymysql*' -o -name 'aiomysql*' -o -name '_sysconfigdata__linux_x86_64-linux-gnu*' -o -name 'loguru*' -o -name 'sqlalchemy*' -o -name 'sniffio*' -o -name 'anyio*' -o -name 'starlette*' -o -name 'fastapi*' -o -name 'certifi*' -o -name 'urllib3*' -o -name 'sentry_sdk*' -o -name 'h11*' -o -name 'multidict*' -o -name 'idna*' -o -name 'yarl*' -o -name 'annotated_types*' -o -name 'dotenv*' -o -name 'pydantic*' -o -name 'pydantic_settings*' -o -name 'click*' \) -exec rm -rf {} +
# remove distutils-precedence.pth if exists
RUN test -f distutils-precedence.pth && rm distutils-precedence.pth || true

WORKDIR /usr/lib/python${PYTHON_VERSION}
RUN python3 -m compileall -o 2 .
RUN find . -name "*.cpython-*.opt-2.pyc" | awk '{print $1, $1}' | sed 's/__pycache__\///2' | sed 's/.cpython-[0-9]\{2,\}.opt-2//2' | xargs -n 2 mv
RUN find . -name "*.py" -delete
RUN find . -name "__pycache__" -exec rm -r {} +

FROM scratch as prod
ARG PYTHON_VERSION=3.10

COPY --from=builder /usr/bin/python3 /

COPY --from=builder /lib/libz.so.1 /lib/
COPY --from=builder /lib/ld-musl-x86_64.so.1 /lib/
COPY --from=builder /usr/lib/libssl.so.3 /usr/lib/
COPY --from=builder /usr/lib/libcrypto.so.3 /usr/lib/
COPY --from=builder /usr/lib/libpython${PYTHON_VERSION}.so.1.0 /usr/lib/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/lib-dynload/ /usr/lib/python${PYTHON_VERSION}/lib-dynload/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/encodings/ /usr/lib/python${PYTHON_VERSION}/encodings/

COPY --from=builder /usr/lib/python${PYTHON_VERSION}/site-packages/ /usr/lib/python${PYTHON_VERSION}/site-packages/

# [AUTO_INSERT_POINT]
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/getpass.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/configparser.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/_sysconfigdata__linux_x86_64-linux-gnu.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/glob.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/sysconfig.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/html/ /usr/lib/python${PYTHON_VERSION}/html/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/colorsys.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/shlex.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/_compression.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/gzip.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/hashlib.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/hmac.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/mimetypes.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/uu.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/textwrap.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/zipfile.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/csv.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/uuid.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/ipaddress.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/dataclasses.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/numbers.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/_pydecimal.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/decimal.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/__future__.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/shutil.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/tempfile.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/multiprocessing/ /usr/lib/python${PYTHON_VERSION}/multiprocessing/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/quopri.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/locale.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/calendar.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/bisect.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/random.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/email/ /usr/lib/python${PYTHON_VERSION}/email/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/platform.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/datetime.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/gettext.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/http/ /usr/lib/python${PYTHON_VERSION}/http/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/urllib/ /usr/lib/python${PYTHON_VERSION}/urllib/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/ntpath.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/fnmatch.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/pathlib.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/base64.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/ssl.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/socketserver.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/copy.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/queue.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/_compat_pickle.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/struct.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/pickle.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/json/ /usr/lib/python${PYTHON_VERSION}/json/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/typing.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/contextvars.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/opcode.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/dis.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/ast.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/inspect.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/signal.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/subprocess.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/selectors.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/socket.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/heapq.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/threading.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/string.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/_weakrefset.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/weakref.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/logging/ /usr/lib/python${PYTHON_VERSION}/logging/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/concurrent/ /usr/lib/python${PYTHON_VERSION}/concurrent/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/asyncio/ /usr/lib/python${PYTHON_VERSION}/asyncio/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/token.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/copyreg.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/sre_constants.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/sre_parse.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/sre_compile.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/enum.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/re.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/linecache.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/tokenize.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/traceback.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/types.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/functools.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/reprlib.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/operator.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/keyword.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/collections/ /usr/lib/python${PYTHON_VERSION}/collections/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/contextlib.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/warnings.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/importlib/ /usr/lib/python${PYTHON_VERSION}/importlib/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/runpy.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/_sitebuiltins.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/genericpath.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/posixpath.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/_collections_abc.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/stat.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/os.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/site.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/abc.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/io.pyc /usr/lib/python${PYTHON_VERSION}/
COPY --from=builder /usr/lib/python${PYTHON_VERSION}/codecs.pyc /usr/lib/python${PYTHON_VERSION}/

WORKDIR /app/src
COPY --from=builder /app/src /app/src

CMD ["/python3", "-m", "sowonpass_backend"]
