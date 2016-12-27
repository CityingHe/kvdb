# -*- coding:utf-8 -*-

class ValueRef(object):
    @staticmethod
    def referent_to_string(referent, storage):
        return referent.encode('utf-8')

    @staticmethod
    def string_to_referent(string):
        return string.decode('utf-8')

    def __init__(self, referent=None, address=0):
        self._referent = referent
        self._address = address

    @property
    def address(self):
        return self._address

    def get(self, storage):
        if self._referent is None and self._address:
            self._referent = self.string_to_referent(storage.read(self._address))
        return self._referent

    def prepare_to_store(self, storage):
        pass

    def store(self, storage):
        # 引用对象不为空而地址为空说明该引用对象还未被存储过
        if self._referent is not None and not self._address:
            # 存储引用对象前的其它操作，自定义
            self.prepare_to_store(storage)
            # 得到引用对象在文件中的地址
            self._address = storage.write(self.referent_to_string(self._referent, storage))
        return self._address

class LogicalBase(object):
    # 对数据结构节点的引用，会在子类中赋值 BinaryNodeRef
    node_ref_class = None
    # 对值的引用
    value_ref_class = ValueRef

    def __init__(self, storage):
        self._storage = storage

    def commit(self):
        self._tree_ref.store(self._storage)
        self._storage.commit_root_address(self._tree_ref.address)

    def _refresh_tree_ref(self):
        self._tree_ref = self.node_ref_class(address=self._storage.get_root_address())

    # 获取键值
    def get(self, key):
        # 如果数据库文件没有上锁，则更新对树的引用
        if not self._storage.locked:
            self._refresh_tree_ref()
        # _get 方法将在子类中实现
        # print self._follow(self._tree_ref), key
        return self._get(self._follow(self._tree_ref), key)

    # 设置键值
    def set(self, key, value):
        if self._storage.lock():
            self._refresh_tree_ref()
        self._tree_ref = self._insert(
            self._follow(self._tree_ref), key, self.value_ref_class(value) )

    # 删除键值
    def pop(self, key):
        if self._storage.lock():
            self._refresh_tree_ref()
        # _delete 方法将在子类中实现
        self._tree_ref = self._delete(
            self._follow(self._tree_ref), key)

    def _follow(self, ref):
        return ref.get(self._storage)

    def __len__(self):
        if not self._storage.locked:
            self._refresh_tree_ref()
        root = self._follow(self._tree_ref)
        if root:
            return root.length
        else:
            return 0