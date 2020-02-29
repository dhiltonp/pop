import abc
import collections
import inspect
import sys
from typing import Any, Dict, Iterator

__func_alias__ = {
    "mutable_namespaced_map": "map",
    "dynamic_mutable_namespaced_map": "dmap",
}


def mutable_namespaced_map(hub, *args, **kwargs):
    class MAP(collections.MutableMapping, abc.ABC):
        """
        An abstract base class that implements the interface of a `dict`
        Items can be set and retrieved via namespacing
        """

        def __init__(self, init: Dict[str, Any] = None, *c_args, **c_kwargs):
            """
            :param init: A dictionary from which to inherit data
            """
            self._store = dict(*c_args, **c_kwargs)
            if init:
                # Existing dictionaries might have values that need wrapped as well
                self.update(init)

        def __setitem__(self, k: str, v: Any):
            """
            Cast all nested dict values as MAP so they get it's benefits as well
            """
            if isinstance(v, dict):
                v = MAP(v)
            self._store[k] = v

        def __delitem__(self, k: str):
            """
            Cleanup method required by abc.ABC
            """
            if k in self._store:
                del self._store[k]

        def __getitem__(self, k: str):
            return self._store[k]

        def __getattr__(self, k: str) -> Any:
            """
            Return dict values on the MAP namespace
            Create the key if it doesn't exist
            """
            if k not in self._store:
                self._store[k] = MAP()
            return self[k]

        def __setattr__(self, k: str, v: Any):
            if k == "_store":
                super().__setattr__(k, v)
            else:
                self[k] = v

        def __len__(self) -> int:
            return len(self._store)

        def __iter__(self) -> Iterator[Any]:
            return iter(self._store)

        def __str__(self) -> str:
            return str(self._store)

    return MAP(*args, **kwargs)


def dynamic_mutable_namespaced_map(hub, *args, **kwargs):
    class DMAP(collections.MutableMapping, abc.ABC):
        """
        An abstract base class that implements the interface of a `dict`

        Stores references to functions that generate the given keys
        When "refresh" is called the reference function is called again
          .. example
            def init(hub):
                hub.grains.GRAINS = hub.pop.data.dmap()

            def load_grain(hub):
                hub.grains.GRAINS.key = "value"

            def exec_module(hub):
                hub.grains.GRAINS.refresh("key")
        """

        def __init__(self, init: Dict[str, Any] = None, *c_args, **c_kwargs):
            """
            :param init: A dictionary from which to inherit data
            """
            self._store = dict(*c_args, **c_kwargs)
            # A reference for the functions that created this value
            self._refs = {}
            if init:
                # Existing dictionaries might have properties that need wrapped as well
                self.update(init)

        async def refresh(self, k: str) -> bool:
            """
            Call the underlying function that generated a grain
            Return true if the value changed, else false
            """
            old_value = self._store.get(k)
            if k in self._refs:
                call = self._refs[k]()

            if hasattr(call, "__await__"):
                await call

            return old_value == self._store.get(k)

        @staticmethod
        def _get_caller():
            """
            This function allows for hub to pop introspective calls.
            This should only ever be called from within a hub module, otherwise
            it should stack trace, or return heaven knows what...
            """
            if hasattr(sys, "_getframe"):
                # implementation detail of CPython, speeds up things by 100x.
                call_frame = sys._getframe(4)
            else:
                call_frame = inspect.stack(0)[4][0]

            return call_frame.f_locals["self"]

        def _setitem(self, k: str, v: Any):
            """
            This needs to exist so that __setattr__ and __setitem__ get the caller at the same level
            """
            if isinstance(v, dict):
                # Cast all nested dict values as DMAP so they get it's benefits as well
                v = DMAP(v)

            self._store[k] = v

            # Find the calling function on the hub and store it in the cache
            self._refs[k] = self._get_caller()

        def __setitem__(self, k: str, v: Any):
            self._setitem(k, v)

        def __delitem__(self, k: str):
            """
            Cleanup method required by abc.ABC
            """
            if k in self._store:
                del self._store[k]
            if k in self._refs:
                del self._refs[k]

        def __getitem__(self, k: str):
            return self._store[k]

        def __getattr__(self, k: str) -> Any:
            """
            Return dict values on the GRAINS namespace
            Create the key if it doesn't exist, this allows nested grains to be created in any order
            i.e. hub.grains.GRAINS.dict_grain.value = property(func)
            """
            if k not in self._store:
                self._store[k] = DMAP()
            return self[k]

        def __setattr__(self, k: str, v: Any):
            if k in ("_refs", "_store"):
                super().__setattr__(k, v)
            else:
                self._setitem(k, v)

        def __len__(self) -> int:
            return len(self._store)

        def __iter__(self) -> Iterator[Any]:
            return iter(self._store)

        def __str__(self) -> str:
            return str(self._store)

    return DMAP(*args, **kwargs)
