def _add_sub_cmd(parent, child_name, help, func=None):
    """
    :type parent: cmdtree.parser.AParser
    :rtype: cmdtree.parser.AParser
    """
    return parent.add_cmd(child_name, help, func)


class CmdTree(object):
    """
    A tree that manages the command references by cmd path like
    ['parent_cmd', 'child_cmd'].
    """

    def __init__(self, root_parser):
        """
        :type root_parser: AParser
        """
        self.root = root_parser
        self.tree = {
            "name": "root",
            "cmd": self.root,
            "children": {}
        }

    @staticmethod
    def _gen_cmd_node(cmd_name, cmd_obj):
        return {
            "name": cmd_name,
            "cmd": cmd_obj,
            "children": {}
        }

    def get_cmd_by_path(self, existed_cmd_path):
        """
        :return:
        {
            "name": cmd_name,
            "cmd": Resource instance,
            "children": {}
        }
        """
        parent = self.tree
        for cmd_name in existed_cmd_path:
            try:
                parent = parent['children'][cmd_name]
            except KeyError:
                raise ValueError(
                    "Given key [%s] in path %s does not exist in tree."
                    % (cmd_name, existed_cmd_path)
                )
        return parent

    def add_node(self, cmd_node, cmd_path):
        """
        :type cmd_path: list or tuple
        """
        parent = self.tree
        for cmd_key in cmd_path:
            if cmd_key not in parent['children']:
                break
            parent = parent['children'][cmd_key]
        parent["children"][cmd_node['name']] = cmd_node
        return cmd_node

    @staticmethod
    def _get_paths(full_path, end_index):
        return full_path[end_index:], full_path[:end_index]

    def add_parent_commands(self, cmd_path):
        """
        Create parent command object in cmd tree then return
        the last parent command object.
        :rtype: dict
        """
        existed_cmd_end_index = self.index_in_tree(cmd_path)
        new_path, existed_path = self._get_paths(
            cmd_path,
            existed_cmd_end_index,
        )
        parent_node = self.get_cmd_by_path(existed_path)
        for cmd_name in new_path:
            sub_cmd = _add_sub_cmd(
                parent_node['cmd'], cmd_name, cmd_name
            )
            parent_node = self._gen_cmd_node(cmd_name, sub_cmd)
            self.add_node(
                parent_node,
                existed_path + new_path[:new_path.index(cmd_name)]
            )
        return parent_node

    def index_in_tree(self, cmd_path):
        """
        Return the start index of which the element is not in cmd tree.
        :type cmd_path: list or tuple
        :return: None if cma_path already indexed in tree.
        """
        current_tree = self.tree
        for key in cmd_path:
            if key in current_tree['children']:
                current_tree = current_tree['children'][key]
            else:
                return cmd_path.index(key)
        return None
