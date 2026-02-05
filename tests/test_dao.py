import unittest
from unittest.mock import patch, mock_open
from data.dao.csv_impl import CSVUsageRecordDAO

class TestCSVUsageRecordDAO(unittest.TestCase):
    def setUp(self):
        # 模拟 CSV 内容
        self.csv_content = (
            '"user_id","feature","efficiency","consumables","comparison","time"\n'
            '"1001","Clean","High","Low","Good","2025-01"\n'
            '"1002","Quiet","Medium","Medium","Fair","2025-01"'
        )

    def test_load_data_success(self):
        with patch("builtins.open", mock_open(read_data=self.csv_content)):
            with patch("os.path.exists", return_value=True):
                dao = CSVUsageRecordDAO("dummy_path.csv")
                
                # 测试存在的记录
                record = dao.get_record("1001", "2025-01")
                self.assertIsNotNone(record)
                self.assertEqual(record["特征"], "Clean")
                self.assertEqual(record["效率"], "High")

                # 测试不存在的用户
                self.assertIsNone(dao.get_record("9999", "2025-01"))
                
                # 测试不存在的月份
                self.assertIsNone(dao.get_record("1001", "2025-02"))

    def test_file_not_found(self):
        with patch("os.path.exists", return_value=False):
            dao = CSVUsageRecordDAO("non_existent.csv")
            # 应该没有任何数据
            self.assertIsNone(dao.get_record("1001", "2025-01"))
