import collections.abc as abc
import inspect
import pop.contract
import sys
from typing import Any, Dict, Iterator, Coroutine

__func_alias__ = {
    "mutable_namespaced_map": "map",
    "dynamic_mutable_namespaced_map": "dmap",
}


def mutable_namespaced_map(hub, *args, **kwargs) -> abc.MutableMapping:
    class MAP(abc.MutableMapping):
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
                assert isinstance(init, Dict)
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


def dynamic_mutable_namespaced_map(hub, *args, **kwargs) -> abc.MutableMapping:
    class DMAP(abc.MutableMapping):
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

        def __init__(
            self,
            init: Dict[str, Any] = None,
            ref: pop.contract.Contracted = None,
            *c_args,
            **c_kwargs,
        ):
            """
            :param init: A dictionary from which to inherit data
            """
            self._store = dict(*c_args, **c_kwargs)
            self._parent_ref = ref
            # A reference for the functions that created this value
            self._ref = {}
            if init:
                # Existing dictionaries might have properties that need wrapped as well
                self.update(init)

        def refresh(self, k: str = None) -> None or Coroutine:
            """
            Call the underlying function that generated a grain,
            If the underlying function was a coroutine, return the awaitable
            """
            # If a key was supplied then call it's ref
            if k in self._ref:
                return self._ref[k]()
            # If refresh was called on this object then access the parent ref
            elif self._parent_ref is not None:
                return self._parent_ref()
            else:
                raise KeyError(
                    f"No function found for '{k}'. Try creating this dmap with a ref"
                )

        def _get_caller(self) -> pop.contract.Contracted:
            """
            This function allows for hub to pop introspective calls.
            This should only ever be called from within a hub module, otherwise
            it should stack trace, or return heaven knows what...
            """
            # Nested values might share a contracted function
            if self._parent_ref is not None:
                return self._parent_ref

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
            # Find the calling function on the hub and store it in the cache
            self._ref[k] = self._get_caller()

            if isinstance(v, dict):
                # Cast all nested dict values as DMAP so they get it's benefits as well
                # Contracts are shared between nested items until they are overridden
                v = DMAP(init=v, ref=self._ref[k])
                self._store[k] = v
            else:
                self._store[k] = v

        def __setitem__(self, k: str, v: Any):
            self._setitem(k, v)

        def __delitem__(self, k: str):
            """
            Cleanup method required by abc.ABC
            """
            if k in self._store:
                del self._store[k]
            if k in self._ref:
                del self._ref[k]

        def __getitem__(self, k: str):
            return self._store[k]

        def __getattr__(self, k: str) -> Any:
            """
            Return dict values on the GRAINS namespace
            Create the key if it doesn't exist, this allows nested grains to be created in any order
            i.e. hub.grains.GRAINS.dict_grain.value = property(func)
            """
            if k not in self._store:
                self._setitem(k, DMAP())

            return self[k]

        def __setattr__(self, k: str, v: Any):
            if k in ("_parent_ref", "_ref", "_store"):
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
