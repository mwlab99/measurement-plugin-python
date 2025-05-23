"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
---------------------------------------------------------------------
---------------------------------------------------------------------
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class Double2DArray(google.protobuf.message.Message):
    """---------------------------------------------------------------------
    Defines a 2D array of values. The 2D array is stored as a repeated field of
    the appropriate element type, a 1D array. It is stored in row major order.

    Example:
    Repeated Double: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    rows: 2
    columns: 5

    2D Representation:
     1  2  3  4  5
     6  7  8  9 10

    Indices:
    (0,0) (0,1) (0,2) (0,3) (0,4)
    (1,0) (1,1) (1,2) (1,3) (1,4)

    Remarks:
     The length of the 'data' field must be equal to rows * columns.
     If it is not, implementations should treat this state as invalid
     and return INVALID_ARGUMENT status code if appropriate.
    ---------------------------------------------------------------------
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ROWS_FIELD_NUMBER: builtins.int
    COLUMNS_FIELD_NUMBER: builtins.int
    DATA_FIELD_NUMBER: builtins.int
    rows: builtins.int
    columns: builtins.int
    @property
    def data(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]: ...
    def __init__(
        self,
        *,
        rows: builtins.int = ...,
        columns: builtins.int = ...,
        data: collections.abc.Iterable[builtins.float] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["columns", b"columns", "data", b"data", "rows", b"rows"]) -> None: ...

global___Double2DArray = Double2DArray

@typing.final
class String2DArray(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ROWS_FIELD_NUMBER: builtins.int
    COLUMNS_FIELD_NUMBER: builtins.int
    DATA_FIELD_NUMBER: builtins.int
    rows: builtins.int
    columns: builtins.int
    @property
    def data(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        rows: builtins.int = ...,
        columns: builtins.int = ...,
        data: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["columns", b"columns", "data", b"data", "rows", b"rows"]) -> None: ...

global___String2DArray = String2DArray
