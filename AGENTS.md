# AI Agent Rules & Guidelines

Tài liệu này định nghĩa các quy tắc bắt buộc mà AI Agent phải tuân thủ khi làm việc và phát triển trên dự án này (kết hợp cùng các rules khác nếu có).

## 1. Đọc tài liệu trước khi hành động
- **Bắt buộc** đọc tài liệu của dự án trước khi đưa ra bất kỳ thay đổi nào (tạo file mới, sửa kiến trúc, tạo database model, v.v).
- **Tuyệt đối không đoán mò**, phải luôn tham chiếu các file tài liệu trong thư mục `docs/` để nắm rõ bối cảnh (context) trước khi code. Cụ thể:
  - **`docs/PROJECT_STRUCTURE.md`**: Đọc để biết vị trí chuẩn xác trước khi tạo hoặc di chuyển một file/thư mục. Không tự ý tạo cấu trúc lạ.
  - **`docs/DATA_MODEL.md`**: Đọc để hiểu về Database schema, các bảng, field, quan hệ (relationships) và các ràng buộc khi làm việc với ORM Model, Schema.
  - **`docs/MVP_SCOPE.md`**: Đọc để nắm vững phạm vi tính năng (scope). Biết rõ những gì cần làm và những gì không thuộc MVP để tránh code thừa.
  - **`docs/ARCHITECTURE.md` & `docs/SYSTEM_DESIGN.md`**: Đọc để rà soát kiến trúc hệ thống, các luồng xử lý (luồng xe vào/ra, luồng camera nhận diện biển số, v.v) trước khi thêm Service logic.
  - **`docs/PROBLEM_DEFINITION.md`**: Đọc để hiểu nghiệp vụ và định nghĩa thực tế của bài toán.
  - **`docs/GETTING_STARTED.md`**: Đọc để biết cách setup và khởi chạy dự án.
## 2. Liên tục cập nhật tài liệu
- Việc code và tài liệu phải luôn song hành với nhau. 
- Nếu trong quá trình phát triển tính năng sinh ra sự thay đổi khác biệt so với tài liệu hiện hành, **luôn luôn sửa đổi, cập nhật docs** (các file `.md` trong thư mục `docs/` hoặc `README.md`) để nội dung phản ánh đúng thực tế code mới nhất.

## 3. Tuân thủ Git Workflow
- Chia nhỏ các công việc. Mỗi khi hoàn thành xong một tính năng nhỏ hoặc một phần công việc độc lập, **luôn thực hiện commit**.
- Định dạng và quy trình commit phải **tuân thủ tuyệt đối luật** được quy định trong file `docs/GIT_WORKFLOW.md`.
## 4. Code Quality & Error Handling (Luật toàn cục)
- Luôn phải có block xử lý lỗi rõ ràng, xử lý trạng thái loading (nếu là UI), và kiểm tra bắt rỗng/null/None dữ liệu một cách đầy đủ.
- Có thể thêm các helper/custom exception xử lý lỗi cho toàn bộ ứng dụng nếu cần.
- **Tư duy tổng thể:** Ưu tiên giải pháp có thể tái sử dụng ứng dụng quy mô toàn hệ thống thay vì code 'chắp vá' chỉ để giải quyết được một task phụ/nhỏ.
## 5. Quy tắc Unit Test & Testing (Bắt buộc)
- ​Việc viết mã nguồn phải luôn đi kèm với việc đảm bảo tính đúng đắn thông qua kiểm thử tự động.
​- Viết Test trước hoặc song hành với Code: * Mọi logic nghiệp vụ (Service), xử lý dữ liệu (Utils) hoặc API endpoint mới được tạo ra bắt buộc phải có file Unit Test tương ứng.
​Ưu tiên tư duy TDD (Test-Driven Development) để xác định đầu vào/đầu ra mong muốn trước khi triển khai logic chi tiết.
​- Vị trí và Đặt tên:
​- Tất cả các file test phải nằm trong thư mục tests/ hoặc theo cấu trúc quy định tại docs/PROJECT_STRUCTURE.md.
- ​Tên file test phải phản ánh đúng file logic cần kiểm tra (Ví dụ: services/auth_service.py đi kèm với tests/test_auth_service.py).
- ​Độ bao phủ (Coverage) & Kịch bản:
- ​Phải kiểm tra ít nhất 2 kịch bản: Happy Path (Dữ liệu chuẩn, thành công) và Edge Cases/Error Handling (Dữ liệu lỗi, null, sai định dạng, quá hạn, v.v.).
- ​Sử dụng Mocking cho các thành phần bên ngoài như Database, Third-party API, hoặc IoT Sensor để đảm bảo Unit Test chạy độc lập và nhanh chóng.
- ​Kiểm tra trước khi Commit:
- ​AI Agent phải tự chạy bộ test hiện có để đảm bảo code mới không làm "gãy" (break) các tính năng cũ.
- ​Nếu phát hiện lỗi trong quá trình chạy test, phải sửa lỗi trước khi thực hiện commit theo docs/GIT_WORKFLOW.md.
